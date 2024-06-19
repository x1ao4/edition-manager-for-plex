import re
import requests

def get_Cut(file_name, server, token, movie_id, language):
    # 定义剪辑版本的英文名称和对应的中文名称
    cuts = {
        r'\b(Theatrical Cut|Theatrical)\b|院线版|院线|公映版|公映': ('Theatrical Cut', '院线版'),
        r'\b(Director\'s Cut|DC)\b|导演剪辑版|导演剪辑': ('Director\'s Cut', '导演剪辑版'),
        r'\b(Producer\'s Cut)\b|制片人剪辑版|制片人剪辑': ('Producer\'s Cut', '制片人剪辑版'),
        r'\b(Extended Cut|Extended)\b|加长版|加长': ('Extended Cut', '加长版'),
        r'\b(Unrated Cut|Unrated)\b|未分级版|未分级': ('Unrated Cut', '未分级版'),
        r'\b(The Final Cut|Final Cut)\b|最终剪辑版|最终剪辑': ('Final Cut', '最终剪辑版'),
        r'\b(Television Cut)\b|电视版': ('Television Cut', '电视版'),
        r'\b(International Cut)\b|国际版': ('International Cut', '国际版'),
        r'\b(Home Video Cut)\b|家庭录像版': ('Home Video Cut', '家庭录像版'),
        r'\b(Rough Cut)\b|初剪版': ('Rough Cut', '初剪版'),
        r'\b(Workprint Cut|Workprint)\b|工作版': ('Workprint Cut', '工作版'),
        r'\b(Fan Edit)\b|粉丝剪辑版|粉丝剪辑': ('Fan Edit', '粉丝剪辑版'),
        r'\b(Redux)\b': ('Redux', '')
    }

    # 遍历所有的剪辑版本，如果在文件名中找到对应的英文名称，就返回对应的中文或英文名称
    for cut_pattern, cut_names in cuts.items():
        if re.search(cut_pattern, file_name, re.IGNORECASE):
            # 如果语言设置为中文，就返回中文名称，否则返回英文名称
            return cut_names[1] if language == 'zh' else cut_names[0]

    # 如果从文件名中获取不到剪辑版本信息，发送请求获取元数据
    headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
    response = requests.get(f'{server}/library/metadata/{movie_id}', headers=headers)
    data = response.json()

    # 从元数据中获取视频流的 title
    part = data['MediaContainer']['Metadata'][0]['Media'][0]['Part'][0]
    if 'Stream' in part:
        video_streams = part['Stream']
        video_stream = next((stream for stream in video_streams if stream['streamType'] == 1), None)
        if video_stream and 'title' in video_stream:
            title = video_stream['title'].upper()
            # 使用和文件名相同的处理方式处理 title
            for cut_pattern, cut_names in cuts.items():
                if re.search(cut_pattern, title, re.IGNORECASE):
                    # 如果语言设置为中文，就返回中文名称，否则返回英文名称
                    return cut_names[1] if language == 'zh' else cut_names[0]

    # 如果没有找到任何剪辑版本信息，就返回 None
    return None
