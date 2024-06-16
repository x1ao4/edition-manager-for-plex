def get_Resolution(metadata):
    # 获取视频流的元数据
    media = metadata.get('Media')
    if media is None or len(media) == 0:
        return None
    video_stream = media[0]

    # 从元数据中获取视频的分辨率
    resolution = video_stream.get('videoResolution')
    if resolution:
        # 将分辨率转换为大写
        resolution = resolution.upper()
        # 如果分辨率是纯数字，添加 "P"
        if resolution.isdigit():
            resolution += 'P'
    return resolution
