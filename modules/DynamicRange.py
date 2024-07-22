import requests

def get_DynamicRange(server, token, movie_id):
    # Send request to get metadata
    headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
    response = requests.get(f'{server}/library/metadata/{movie_id}', headers=headers)
    data = response.json()

    # Get the title of the video stream from the metadata
    part = data['MediaContainer']['Metadata'][0]['Media'][0]['Part'][0]
    if 'Stream' in part:
        video_streams = part['Stream']
        video_stream = next((stream for stream in video_streams if stream['streamType'] == 1), None)
        if video_stream and 'displayTitle' in video_stream:
            # Extract displayTitle from MediaContainer
            display_title = video_stream['displayTitle']

            # Initialize dynamic range as SDR
            dynamicrange = 'SDR'

            # Check if displayTitle contains 'HDR' or 'DoVi'
            if 'HDR' in display_title and 'DoVi' in display_title and 'DOVIProfile' in video_stream:
                dovi_profile = video_stream['DOVIProfile']
                dynamicrange = f'HDR · DV P{dovi_profile}'
            elif 'HDR' in display_title:
                dynamicrange = 'HDR'
            elif 'DoVi' in display_title and 'DOVIProfile' in video_stream:
                dovi_profile = video_stream['DOVIProfile']
                dynamicrange = f'DV P{dovi_profile}'

            return dynamicrange

    # If no video stream is found, return None
    return None