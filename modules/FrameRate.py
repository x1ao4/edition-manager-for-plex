def get_FrameRate(metadata):
    # 获取视频流的元数据
    media = metadata.get('Media')
    if media is None or len(media) == 0:
        return None
    video_stream = media[0]

    # 获取视频帧率，如果不存在则返回 None
    video_framerate = video_stream.get('videoFrameRate')

    if video_framerate is not None:
        # 将视频帧率转为大写
        video_framerate_upper = video_framerate.upper()

        # 如果视频帧率是 NTSC，则返回 30P
        if video_framerate_upper == 'NTSC':
            return '30P'
        # 如果视频帧率是 PAL，则返回 25P
        elif video_framerate_upper == 'PAL':
            return '25P'
        # 如果视频帧率是 FILM，则返回 24P
        elif video_framerate_upper == 'FILM':
            return '24P'
        else:
            return video_framerate_upper
