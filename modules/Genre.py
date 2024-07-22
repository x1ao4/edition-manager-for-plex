def get_Genre(metadata):
    genres = metadata.get('Genre', [])
    if genres:
        return genres[0].get('tag')
    return None