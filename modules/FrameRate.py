def get_FrameRate(metadata):
    media = metadata.get('Media')
    if media is None or len(media) == 0:
        return None
    video_stream = media[0]

    video_framerate = video_stream.get('videoFrameRate')

    if video_framerate is not None:
        video_framerate_upper = video_framerate.upper()

        if video_framerate_upper == 'NTSC':
            return '30P'
        elif video_framerate_upper == 'PAL':
            return '25P'
        elif video_framerate_upper == 'FILM':
            return '24P'
        else:
            return video_framerate_upper