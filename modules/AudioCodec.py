import requests

def get_AudioCodec(server, token, movie_id, language):
    # 发送请求获取元数据
    headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
    response = requests.get(f'{server}/library/metadata/{movie_id}', headers=headers)
    data = response.json()

    # 从元数据中获取视频流的 title
    part = data['MediaContainer']['Metadata'][0]['Media'][0]['Part'][0]
    if 'Stream' in part:
        # 提取所有音频流
        audio_streams = [stream for stream in part['Stream'] if stream['streamType'] == 2]
        if audio_streams:
            # 按照声道数排序，如果声道数相同，则按照比特率排序
            audio_streams.sort(key=lambda x: (x.get('channels', 0), x.get('bitrate', 0)), reverse=True)
            
            audio_info = audio_streams[0]['displayTitle']
            # 从 displayTitle 中提取最后一组括号内的部分作为音频信息
            last_parenthesis_start = audio_info.rfind("(")
            last_parenthesis_end = audio_info.rfind(")")
            if last_parenthesis_start != -1 and last_parenthesis_end != -1:
                audio_info = audio_info[last_parenthesis_start+1:last_parenthesis_end]
            else:
                audio_info = audio_info
            
            # 如果语言是中文，将 "Mono" 和 "Stereo" 翻译为中文
            if language == 'zh':
                audio_info = audio_info.replace('Mono', '单声道')
                audio_info = audio_info.replace('Stereo', '立体声')
            
            return audio_info

    # 如果没有找到任何音频流，就返回 None
    return None
