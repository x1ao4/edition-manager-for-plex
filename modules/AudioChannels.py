def get_AudioChannels(metadata):
    if 'Media' in metadata and metadata['Media']:
        audio_channels = metadata['Media'][0].get('audioChannels')
        if audio_channels:
            channel_map = {2: '2.0', 6: '5.1', 8: '7.1'}
            return channel_map.get(audio_channels, f'{audio_channels}.0')
    return None