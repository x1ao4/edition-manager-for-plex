import requests

def get_Size(server, token, movie_id):
    headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
    response = requests.get(f'{server}/library/metadata/{movie_id}', headers=headers)
    data = response.json()

    max_size = 0

    for media in data['MediaContainer']['Metadata'][0]['Media']:
        for part in media['Part']:
            if part['size'] > max_size:
                max_size = part['size']

    if max_size < 1024:
        return f"{max_size} B"
    elif max_size < 1024**2:
        return f"{max_size/1024:.2f} KB"
    elif max_size < 1024**3:
        return f"{max_size/1024**2:.2f} MB"
    else:
        return f"{max_size/1024**3:.2f} GB"