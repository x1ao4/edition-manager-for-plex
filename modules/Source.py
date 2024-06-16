import re
import requests

def get_Source(file_name, server, token, movie_id):
    # 定义一个内部函数来匹配片源版本
    def match_source(title):
        if re.search(r'\b(REMUX|BDREMUX|BD-REMUX)\b', title):
            return 'REMUX'
        elif re.search(r'\b(BLURAY|BD|BLU-RAY|BD1080P)\b|蓝光', title):
            return 'BD'
        elif re.search(r'\bBDRIP\b', title):
            return 'BDRIP'
        elif re.search(r'\bWEB-DL|WEBDL\b', title):
            return 'WEB-DL'
        elif re.search(r'\bVODRIP\b', title):
            return 'VODRIP'
        elif re.search(r'\bWEBRIP\b', title):
            return 'WEBRIP'
        elif re.search(r'\bHDRIP\b', title):
            return 'HDRIP'
        elif re.search(r'\bHR-HDTV|HRHDTV\b', title):
            return 'HR-HDTV'
        elif re.search(r'\bHDTV\b', title):
            return 'HDTV'
        elif re.search(r'\bPDTV\b', title):
            return 'PDTV'
        elif re.search(r'\bDVD\b', title):
            return 'DVD'
        elif re.search(r'\bDVDRIP\b', title):
            return 'DVDRIP'
        elif re.search(r'\bDVDSCR\b', title):
            return 'DVDSCR'
        elif re.search(r'\bR5\b', title):
            return 'R5'
        elif re.search(r'\bLDRIP\b', title):
            return 'LDRIP'
        elif re.search(r'\bPPVRIP\b', title):
            return 'PPVRIP'
        elif re.search(r'\bSDTV\b', title):
            return 'SDTV'
        elif re.search(r'\bTVRIP\b', title):
            return 'TVRIP'
        elif re.search(r'\bVHSRIP\b', title):
            return 'VHSRIP'
        elif re.search(r'\bHDTC|HD-TC\b', title):
            return 'HDTC'
        elif re.search(r'\bTC\b', title) and not title.endswith('.TC'):
            return 'TC'
        elif re.search(r'\bHDCAM|HD-CAM\b', title):
            return 'HDCAM'
        elif re.search(r'\bHQCAM|HQ-CAM\b', title):
            return 'HQCAM'
        elif re.search(r'\bTS\b', title) and not title.endswith('.TS'):
            return 'TS'
        elif re.search(r'\bCAM\b', title):
            return 'CAM'
        else:
            return None

    # 首先尝试从文件名中获取片源版本信息
    source = match_source(file_name.upper())

    # 如果从文件名中获取不到片源版本信息，发送请求获取元数据
    if source is None:
        headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
        response = requests.get(f'{server}/library/metadata/{movie_id}', headers=headers)
        data = response.json()

        # 从元数据中获取视频流的 title
        part = data['MediaContainer']['Metadata'][0]['Media'][0]['Part'][0]
        if 'Stream' in part:
            video_streams = part['Stream']
            video_stream = next((stream for stream in video_streams if stream['streamType'] == 1), None)
            if video_stream and 'title' in video_stream:
                # 使用和处理文件名相同的方式处理 title
                source = match_source(video_stream['title'].upper())

    return source
