def get_ContentRating(metadata):
    # Get content rating information from metadata
    contentRating = metadata.get('contentRating', None)

    # If content rating is "Not Rated", convert it to "NR"
    if contentRating == 'Not Rated':
        contentRating = 'NR'

    return contentRating