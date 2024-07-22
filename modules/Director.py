def get_Director(metadata):
    directors = metadata.get('Director', [])
    if directors:
        return directors[0].get('tag')  # Return only the first director
    return None