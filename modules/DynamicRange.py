import requests

def get_DynamicRange(server, token, movie_id):
    # 发送请求获取元数据
    headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
    response = requests.get(f'{server}/library/metadata/{movie_id}', headers=headers)
    data = response.json()

    # 从元数据中获取视频流的 title
    part = data['MediaContainer']['Metadata'][0]['Media'][0]['Part'][0]
    if 'Stream' in part:
        video_streams = part['Stream']
        video_stream = next((stream for stream in video_streams if stream['streamType'] == 1), None)
        if video_stream and 'displayTitle' in video_stream:
            # 从 MediaContainer 中提取 displayTitle
            display_title = video_stream['displayTitle']

            # 初始化动态范围为 SDR
            dynamicrange = 'SDR'

            # 检查 displayTitle 是否包含 'HDR' 或 'DoVi'
            if 'HDR' in display_title and 'DoVi' in display_title and 'DOVIProfile' in video_stream:
                dovi_profile = video_stream['DOVIProfile']
                dynamicrange = f'HDR · DV P{dovi_profile}'
            elif 'HDR' in display_title:
                dynamicrange = 'HDR'
            elif 'DoVi' in display_title and 'DOVIProfile' in video_stream:
                dovi_profile = video_stream['DOVIProfile']
                dynamicrange = f'DV P{dovi_profile}'

            return dynamicrange

    # 如果没有找到任何视频流，就返回 None
    return None
