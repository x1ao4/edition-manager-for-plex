import re
import requests

def get_Release(file_name, server, token, movie_id, language):
    # 定义发行版本的英文名称和对应的中文名称
    releases = {
        r'\b(Special Edition)\b|特别版': ('Special Edition', '特别版'),
        r'\b(Restored Edition)\b|数字修复版|数字修复': ('Restored Edition', '数字修复版'),
        r'\b(3D Edition|3D)\b|3D版': ('3D Edition', '3D 版'),
        r'\b(IMAX Edition|IMAX)\b|IMAX版': ('IMAX Edition', 'IMAX 版'),
        r'\b(Collector\'s Edition)\b|收藏版': ('Collector\'s Edition', '收藏版'),
        r'\b(Anniversary Edition)\b|周年纪念版': ('Anniversary Edition', '周年纪念版'),
        r'\b(Ultimate Edition)\b|终极版': ('Ultimate Edition', '终极版'),
        r'\b(Blu-ray Edition|Blu-ray|Bluray|BD)\b|蓝光版|蓝光': ('Blu-ray Edition', '蓝光版'),
        r'\b(DVD Edition|DVD)\b|DVD版': ('DVD Edition', 'DVD 版'),
        r'\b(Limited Edition|Limited)\b|限量版': ('Limited Edition', '限量版'),
        r'\b(Commemorative Edition)\b|纪念版': ('Commemorative Edition', '纪念版'),
        r'\b(Deluxe Edition)\b|豪华版': ('Deluxe Edition', '豪华版'),
        r'\b(Director\'s Signature Edition|Director\'s Signature)\b|导演签名版': ('Director\'s Signature Edition', '导演签名版'),
        r'\b(Criterion Collection|CC)\b|标准收藏版|标准收藏': ('Criterion Collection', '标准收藏版')
    }

    # 创建一个列表来存储所有匹配到的发行版本
    matched_releases = []

    # 遍历所有的发行版本，如果在文件名中找到对应的英文名称，就添加到列表中
    for release_pattern, release_names in releases.items():
        if re.search(release_pattern, file_name, re.IGNORECASE):
            # 如果语言设置为中文，就添加中文名称，否则添加英文名称
            matched_releases.append(release_names[1] if language == 'zh' else release_names[0])

    # 如果从文件名中获取不到发行版本信息，发送请求获取元数据
    if not matched_releases:
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
                for release_pattern, release_names in releases.items():
                    if re.search(release_pattern, title, re.IGNORECASE):
                        # 如果语言设置为中文，就添加中文名称，否则添加英文名称
                        matched_releases.append(release_names[1] if language == 'zh' else release_names[0])

    # 如果没有找到任何发行版本信息，就返回 None
    return ' · '.join(matched_releases) if matched_releases else None
