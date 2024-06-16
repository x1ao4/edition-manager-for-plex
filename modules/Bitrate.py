import requests

def get_Bitrate(server, token, movie_id):
    # 发送请求获取元数据
    headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
    response = requests.get(f'{server}/library/metadata/{movie_id}', headers=headers)
    data = response.json()

    # 初始化最大文件大小为0
    max_size = 0
    max_bitrate = None

    # 遍历每个 Media 对象
    for media in data['MediaContainer']['Metadata'][0]['Media']:
        # 遍历每个 Part 对象
        for part in media['Part']:
            # 如果这个 Part 的文件大小大于当前的最大文件大小，就更新最大文件大小和比特率
            if part['size'] > max_size:
                max_size = part['size']
                max_bitrate = media.get('bitrate')

    # 如果没有找到任何视频文件，返回 None
    if max_bitrate is None:
        return None

    # 将比特率从 Kbps 转换为 Mbps
    video_bitrate_mbps = max_bitrate / 1000
    # 如果比特率小于 1 Mbps，则使用 Kbps 作为单位，并四舍五入到整数
    if video_bitrate_mbps < 1:
        return f"{round(max_bitrate)} Kbps"
    else:
        # 四舍五入到小数点后一位，并使用 Mbps 作为单位
        return f"{round(video_bitrate_mbps, 1)} Mbps"
