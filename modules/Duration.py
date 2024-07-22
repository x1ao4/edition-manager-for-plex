def get_Duration(metadata):
    # Get metadata for the video stream
    media = metadata.get('Media')
    if media is None or len(media) == 0:
        return None
    video_stream = media[0]

    # Get the duration of the video from the metadata (in milliseconds)
    duration_ms = video_stream.get('duration')
    if duration_ms is None:
        return None

    # Convert duration from milliseconds to minutes, and round to the nearest integer
    duration_min = round(duration_ms / 1000 / 60)

    return f"{duration_min} MIN"