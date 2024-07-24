import requests

def get_AudioCodec(server, token, movie_id):
    headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
    response = requests.get(f'{server}/library/metadata/{movie_id}', headers=headers)
    data = response.json()

    part = data['MediaContainer']['Metadata'][0]['Media'][0]['Part'][0]
    if 'Stream' in part:
        audio_streams = [stream for stream in part['Stream'] if stream['streamType'] == 2]
        if audio_streams:
            audio_streams.sort(key=lambda x: (x.get('channels', 0), x.get('bitrate', 0)), reverse=True)
            
            audio_info = audio_streams[0]['displayTitle']
            last_parenthesis_start = audio_info.rfind("(")
            last_parenthesis_end = audio_info.rfind(")")
            if last_parenthesis_start != -1 and last_parenthesis_end != -1:
                audio_info = audio_info[last_parenthesis_start+1:last_parenthesis_end]
            
            return audio_info

    return None