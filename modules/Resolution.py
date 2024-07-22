def get_Resolution(metadata):
    # Get metadata for the video stream
    media = metadata.get('Media')
    if media is None or len(media) == 0:
        return None
    video_stream = media[0]

    # Get the resolution of the video from the metadata
    resolution = video_stream.get('videoResolution')
    if resolution:
        # Convert resolution to uppercase
        resolution = resolution.upper()
        # If resolution is purely numeric, add "p"
        if resolution.isdigit():
            resolution += 'p'
    return resolution