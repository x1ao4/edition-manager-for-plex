def get_VideoCodec(metadata):
    media = metadata.get('Media')
    if media is None or len(media) == 0:
        return None
    video_stream = media[0]

    video_codec = video_stream.get('videoCodec')

    if video_codec is not None:
        video_codec = video_codec.upper()
        if video_codec == 'MPEG2VIDEO':
            video_codec = 'MPEG2'
        elif video_codec == 'MPEG1VIDEO':
            video_codec = 'MPEG1'

    return video_codec