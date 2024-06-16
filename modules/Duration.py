def get_Duration(metadata, language):
    # 获取视频流的元数据
    media = metadata.get('Media')
    if media is None or len(media) == 0:
        return None
    video_stream = media[0]

    # 从元数据中获取视频的时长（单位：毫秒）
    duration_ms = video_stream.get('duration')
    if duration_ms is None:
        return None

    # 将时长从毫秒转换为分钟，并四舍五入到最接近的整数
    duration_min = round(duration_ms / 1000 / 60)

    # 根据用户选择的语言返回不同的单位
    if language == 'zh':
        return f"{duration_min} 分钟"
    elif language == 'en':
        return f"{duration_min} MIN"
