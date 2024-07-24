import requests

def get_Bitrate(server, token, movie_id):
    headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
    response = requests.get(f'{server}/library/metadata/{movie_id}', headers=headers)
    data = response.json()

    max_size = 0
    max_bitrate = None

    for media in data['MediaContainer']['Metadata'][0]['Media']:
        for part in media['Part']:
            if part['size'] > max_size:
                max_size = part['size']
                max_bitrate = media.get('bitrate')

    if max_bitrate is None:
        return None

    video_bitrate_mbps = max_bitrate / 1000
    if video_bitrate_mbps < 1:
        return f"{round(max_bitrate)} Kbps"
    else:
        return f"{round(video_bitrate_mbps, 1)} Mbps"