import re
import requests

def get_Source(file_name, server, token, movie_id):
    def match_source(title):
        sources = {
            r'\b(REMUX|BDREMUX|BD-REMUX)\b': 'REMUX',
            r'\b(BLURAY|BD|BLU-RAY|BD1080P)\b': 'BD',
            r'\bBDRIP\b': 'BDRIP',
            r'\bWEB-DL|WEBDL\b': 'WEB-DL',
            r'\bVODRIP\b': 'VODRIP',
            r'\bWEBRIP\b': 'WEBRIP',
            r'\bHDRIP\b': 'HDRIP',
            r'\bHR-HDTV|HRHDTV\b': 'HR-HDTV',
            r'\bHDTV\b': 'HDTV',
            r'\bPDTV\b': 'PDTV',
            r'\bDVD\b': 'DVD',
            r'\bDVDRIP\b': 'DVDRIP',
            r'\bDVDSCR\b': 'DVDSCR',
            r'\bR5\b': 'R5',
            r'\bLDRIP\b': 'LDRIP',
            r'\bPPVRIP\b': 'PPVRIP',
            r'\bSDTV\b': 'SDTV',
            r'\bTVRIP\b': 'TVRIP',
            r'\bVHSRIP\b': 'VHSRIP',
            r'\bHDTC|HD-TC\b': 'HDTC',
            r'\bTC\b': 'TC',
            r'\bHDCAM|HD-CAM\b': 'HDCAM',
            r'\bHQCAM|HQ-CAM\b': 'HQCAM',
            r'\bTS\b': 'TS',
            r'\bCAM\b': 'CAM'
        }
        for pattern, source in sources.items():
            if re.search(pattern, title, re.IGNORECASE):
                return source
        return None

    source = match_source(file_name.upper())

    if source is None:
        headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
        response = requests.get(f'{server}/library/metadata/{movie_id}', headers=headers)
        data = response.json()

        part = data['MediaContainer']['Metadata'][0]['Media'][0]['Part'][0]
        if 'Stream' in part:
            video_streams = part['Stream']
            video_stream = next((stream for stream in video_streams if stream['streamType'] == 1), None)
            if video_stream and 'title' in video_stream:
                source = match_source(video_stream['title'].upper())

    return source