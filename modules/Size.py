import requests

def get_Size(server, token, movie_id):
    # 发送请求获取元数据
    headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
    response = requests.get(f'{server}/library/metadata/{movie_id}', headers=headers)
    data = response.json()

    # 初始化最大文件大小为0
    max_size = 0

    # 遍历每个 Media 对象
    for media in data['MediaContainer']['Metadata'][0]['Media']:
        # 遍历每个 Part 对象
        for part in media['Part']:
            # 如果这个 Part 的文件大小大于当前的最大文件大小，就更新最大文件大小
            if part['size'] > max_size:
                max_size = part['size']

    # 将文件大小从字节转换为更易读的格式
    if max_size < 1024:
        return f"{max_size} B"
    elif max_size < 1024**2:
        return f"{max_size/1024:.2f} KB"
    elif max_size < 1024**3:
        return f"{max_size/1024**2:.2f} MB"
    else:
        return f"{max_size/1024**3:.2f} GB"
