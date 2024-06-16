def get_VideoCodec(metadata):
    # 获取视频流的元数据
    media = metadata.get('Media')
    if media is None or len(media) == 0:
        return None
    video_stream = media[0]

    # 获取视频编码
    video_codec = video_stream.get('videoCodec')

    # 将视频编码转为大写，如果视频编码存在的话
    if video_codec is not None:
        video_codec = video_codec.upper()
        # 检查是否为 MPEG2VIDEO 或 MPEG1VIDEO 并转换
        if video_codec == 'MPEG2VIDEO':
            video_codec = 'MPEG2'
        elif video_codec == 'MPEG1VIDEO':
            video_codec = 'MPEG1'

    return video_codec
