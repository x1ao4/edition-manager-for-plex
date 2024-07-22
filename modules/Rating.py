import requests
from configparser import ConfigParser
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_Rating(metadata, server, token, movie_id):
    config = ConfigParser()
    config.read('config/config.ini')
    
    rating_source = config.get('rating', 'source', fallback='imdb').lower()
    tmdb_api_key = config.get('rating', 'tmdb_api_key', fallback=None)

    if rating_source == 'imdb':
        return get_tmdb_rating(metadata, tmdb_api_key)
    elif rating_source == 'rotten_tomatoes':
        return get_rotten_tomatoes_rating(server, token, movie_id)
    else:
        return None

def get_tmdb_rating(metadata, tmdb_api_key):
    if not tmdb_api_key:
        logger.error("TMDb API key is missing. Please add it to your config.ini file.")
        return None

    title = metadata.get('title')
    year = metadata.get('year')

    if not title or not year:
        logger.warning(f"Missing title or year for movie: {title} ({year})")
        return None

    logger.info(f"Searching for movie: {title} ({year})")
    
    # Search for the movie on TMDb
    search_url = f"https://api.themoviedb.org/3/search/movie?api_key={tmdb_api_key}&query={title}&year={year}"
    try:
        response = requests.get(search_url)
        response.raise_for_status()
        search_data = response.json()
        
        if search_data['results']:
            movie = search_data['results'][0]
            rating = movie.get('vote_average')
            if rating:
                formatted_rating = f"{rating:.1f}"  # Format to one decimal place
                logger.info(f"Rating for {title} ({year}): {formatted_rating}")
                return formatted_rating
            else:
                logger.info(f"No rating found for {title} ({year})")
        else:
            logger.warning(f"No results found for {title} ({year})")
    except Exception as e:
        logger.error(f"Error fetching rating for {title} ({year}): {str(e)}")
    
    return None

def get_rotten_tomatoes_rating(server, token, movie_id):
    headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
    response = requests.get(f'{server}/library/metadata/{movie_id}', headers=headers)
    data = response.json()

    if 'MediaContainer' in data and 'Metadata' in data['MediaContainer']:
        metadata = data['MediaContainer']['Metadata'][0]
        rating = metadata.get('rating')
        if rating:
            percentage = int(float(rating) * 10)
            return f"{percentage}%"

    return None