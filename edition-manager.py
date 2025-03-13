import os
import re
import sys
import time
import json
import logging
import requests
import argparse
import threading
import queue
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from configparser import ConfigParser
from diskcache import Cache

# Initialize a cache with 1GB limit, expiring items after 1 day
cache = Cache(directory=str(Path(__file__).parent / 'cache'), size_limit=1024 * 1024 * 1024, 
              eviction_policy='least-recently-used', cull_limit=10, 
              statistics=True, tag_index=True, timeout=60)

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Thread-local storage for requests session
thread_local = threading.local()

def get_session():
    """Get thread-local session for connection pooling"""
    if not hasattr(thread_local, "session"):
        thread_local.session = requests.Session()
    return thread_local.session

# Cached API request function
def cached_request(url, headers, cache_key=None, force_refresh=False):
    """Make a cached API request"""
    if not cache_key:
        cache_key = f"request:{url}"
    
    if not force_refresh and cache_key in cache:
        logger.debug(f"Cache hit for {url}")
        return cache[cache_key]
    
    session = get_session()
    response = session.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()
    
    # Cache the response
    cache[cache_key] = data
    return data

# Initialize settings
def initialize_settings():
    config_file = Path(__file__).parent / 'config' / 'config.ini'
    config = ConfigParser()
    config.read(config_file)
    if 'server' in config.sections():
        server = config.get('server', 'address')
        token = config.get('server', 'token')
        skip_libraries = set(re.split(r'[；;]', config.get('server', 'skip_libraries'))) if config.has_option('server', 'skip_libraries') else set()
        modules = re.split(r'[；;]', config.get('modules', 'order')) if config.has_option('modules', 'order') else ['Resolution', 'Duration', 'Rating', 'Cut', 'Release', 'DynamicRange', 'Country', 'ContentRating', 'Language', 'AudioChannels', 'Director', 'Genre', 'SpecialFeatures', 'Studio', 'AudioCodec', 'Bitrate', 'FrameRate', 'Size', 'Source', 'VideoCodec']
        
        excluded_languages = set()
        if config.has_option('language', 'excluded_languages'):
            excluded_languages = set(lang.strip() for lang in re.split(r'[,;]', config.get('language', 'excluded_languages')))
        
        # Performance settings
        max_workers = config.getint('performance', 'max_workers', fallback=10)
        batch_size = config.getint('performance', 'batch_size', fallback=25)
        
        try:
            # Test connection using cached request with forced refresh
            headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
            response = cached_request(server, headers, "server_connection", force_refresh=True)
            server_name = response['MediaContainer']['friendlyName']
            logger.info(f"Successfully connected to server: {server_name}")
        except requests.exceptions.RequestException as err:
            logger.error("Server connection failed, please check the settings in the configuration file or your network. For help, please visit https://github.com/x1ao4/edition-manager-for-plex for instructions.")
            time.sleep(10)
            raise SystemExit(err)
        return server, token, skip_libraries, modules, excluded_languages, max_workers, batch_size

# Batched movie processing
def process_movies_batch(movies_batch, server, token, modules, excluded_languages, lib_title=""):
    """Process a batch of movies in parallel"""
    for movie in movies_batch:
        try:
            process_single_movie(server, token, movie, modules, excluded_languages)
        except Exception as e:
            logger.error(f"Error processing movie {movie.get('title', 'Unknown')}: {str(e)}")

# Main movie processing function (now with threading)
def process_movies(server, token, skip_libraries, modules, excluded_languages, max_workers, batch_size):
    headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
    libraries = cached_request(f'{server}/library/sections', headers)['MediaContainer']['Directory']
    
    # Get all movies from all movie libraries first
    all_movies = []
    library_info = {}
    
    for library in libraries:
        if library['type'] == 'movie' and library['title'] not in skip_libraries:
            library_key = library['key']
            lib_title = library['title']
            
            response = cached_request(f'{server}/library/sections/{library_key}/all', headers)
            if 'MediaContainer' in response and 'Metadata' in response['MediaContainer']:
                library_movies = response['MediaContainer']['Metadata']
                all_movies.extend(library_movies)
                library_info[lib_title] = len(library_movies)
                
    logger.info(f"Total movies to process: {len(all_movies)}")
    for lib_title, count in library_info.items():
        logger.info(f'Library: {lib_title}, Movie count: {count}')
    
    # Process in batches with ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i in range(0, len(all_movies), batch_size):
            batch = all_movies[i:i+batch_size]
            executor.submit(process_movies_batch, batch, server, token, modules, excluded_languages)
            logger.info(f"Submitted batch {i//batch_size + 1}/{(len(all_movies)+batch_size-1)//batch_size} for processing")

# Process a single movie (with caching)
def process_single_movie(server, token, movie, modules, excluded_languages):
    headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
    movie_id = movie['ratingKey']
    
    # Use cached metadata when possible (per movie)
    movie_cache_key = f"movie:{movie_id}"
    
    # Check if detailed movie data is already in cache
    detailed_movie = None
    if movie_cache_key in cache:
        detailed_movie = cache[movie_cache_key]
    else:
        # Need to fetch detailed info
        detailed_response = get_session().get(f'{server}/library/metadata/{movie_id}', headers=headers)
        if detailed_response.status_code == 200:
            detailed_data = detailed_response.json()
            if 'MediaContainer' in detailed_data and 'Metadata' in detailed_data['MediaContainer']:
                detailed_movie = detailed_data['MediaContainer']['Metadata'][0]
                # Cache the detailed movie data
                cache[movie_cache_key] = detailed_movie
    
    # Use detailed_movie when available, otherwise fall back to basic movie data
    movie_data = detailed_movie if detailed_movie else movie
    
    media_parts = movie_data['Media'][0]['Part']
    if media_parts:
        max_size_part = max(media_parts, key=lambda part: part['size'])
        file_path = max_size_part['file']
        file_name = os.path.basename(file_path)
        tags = []
        
        from modules.Resolution import get_Resolution
        from modules.Duration import get_Duration
        from modules.Rating import get_Rating
        from modules.Cut import get_Cut
        from modules.Release import get_Release
        from modules.DynamicRange import get_DynamicRange
        from modules.Country import get_Country
        from modules.ContentRating import get_ContentRating
        from modules.Language import get_Language
        from modules.AudioChannels import get_AudioChannels
        from modules.Director import get_Director
        from modules.Genre import get_Genre
        from modules.SpecialFeatures import get_SpecialFeatures
        from modules.Studio import get_Studio
        from modules.AudioCodec import get_AudioCodec
        from modules.Bitrate import get_Bitrate
        from modules.FrameRate import get_FrameRate
        from modules.Size import get_Size
        from modules.Source import get_Source
        from modules.VideoCodec import get_VideoCodec
        
        # Process each module
        for module in modules:
            try:
                if module == 'Resolution':
                    Resolution = get_Resolution(movie_data)
                    if Resolution:
                        tags.append(Resolution)
                elif module == 'Duration':
                    Duration = get_Duration(movie_data)
                    if Duration:
                        tags.append(Duration)
                elif module == 'Rating':
                    Rating = get_Rating(movie_data, server, token, movie_id)
                    if Rating:
                        tags.append(Rating)
                elif module == 'Cut':
                    Cut = get_Cut(file_name, server, token, movie_id)
                    if Cut:
                        tags.append(Cut)
                elif module == 'Release':
                    Release = get_Release(file_name, server, token, movie_id)
                    if Release:
                        tags.append(Release)
                elif module == 'DynamicRange':
                    DynamicRange = get_DynamicRange(server, token, movie_id)
                    if DynamicRange:
                        tags.append(DynamicRange)
                elif module == 'Country':
                    Country = get_Country(server, token, movie_id)
                    if Country:
                        tags.append(Country)
                elif module == 'ContentRating':
                    ContentRating = get_ContentRating(movie_data)
                    if ContentRating:
                        tags.append(ContentRating)
                elif module == 'Language':
                    Language = get_Language(server, token, movie_id, excluded_languages)
                    if Language:
                        tags.append(Language)
                elif module == 'AudioChannels':
                    AudioChannels = get_AudioChannels(movie_data)
                    if AudioChannels:
                        tags.append(AudioChannels)
                elif module == 'Director':
                    Director = get_Director(movie_data)
                    if Director:
                        tags.append(Director)
                elif module == 'Genre':
                    Genre = get_Genre(movie_data)
                    if Genre:
                        tags.append(Genre)
                elif module == 'SpecialFeatures':
                    SpecialFeatures = get_SpecialFeatures(movie_data)
                    if SpecialFeatures:
                        tags.append(SpecialFeatures)
                elif module == 'Studio':
                    Studio = get_Studio(movie_data)
                    if Studio:
                        tags.append(Studio)
                elif module == 'AudioCodec':
                    AudioCodec = get_AudioCodec(server, token, movie_id)
                    if AudioCodec:
                        tags.append(AudioCodec)
                elif module == 'Bitrate':
                    Bitrate = get_Bitrate(server, token, movie_id)
                    if Bitrate:
                        tags.append(Bitrate)
                elif module == 'FrameRate':
                    FrameRate = get_FrameRate(movie_data)
                    if FrameRate:
                        tags.append(FrameRate)
                elif module == 'Size':
                    Size = get_Size(server, token, movie_id)
                    if Size:
                        tags.append(Size)
                elif module == 'Source':
                    Source = get_Source(file_name, server, token, movie_id)
                    if Source:
                        tags.append(Source)
                elif module == 'VideoCodec':
                    VideoCodec = get_VideoCodec(movie_data)
                    if VideoCodec:
                        tags.append(VideoCodec)
            except Exception as e:
                logger.error(f"Error processing module {module} for {movie_data.get('title', 'Unknown')}: {str(e)}")
        
        # Always call update_movie, even if tags is empty
        update_movie(server, token, movie_data, tags, modules)

def update_movie(server, token, movie, tags, modules):
    movie_id = movie['ratingKey']
    title = movie.get('title', 'Unknown')
    
    # Clear existing edition title and rating
    clear_params = {
        'type': 1,
        'id': movie_id,
        'editionTitle.value': '',
        'editionTitle.locked': 0,
        'rating.value': '',
        'rating.locked': 0
    }
    
    session = get_session()
    session.put(f'{server}/library/metadata/{movie_id}', headers={'X-Plex-Token': token}, params=clear_params)
    
    # Remove duplicates while preserving order
    tags = list(dict.fromkeys(tags))

    if tags:
        edition_title = ' · '.join(tags)
        params = {
            'type': 1,
            'id': movie_id,
            'editionTitle.value': edition_title,
            'editionTitle.locked': 1
        }
        
        # If 'Rating' is in modules, add it to params
        if 'Rating' in modules and any(tag.replace('.', '').isdigit() for tag in tags):
            rating = next(tag for tag in tags if tag.replace('.', '').isdigit())
            params['rating.value'] = rating
            params['rating.locked'] = 1
        
        session.put(f'{server}/library/metadata/{movie_id}', headers={'X-Plex-Token': token}, params=params)
        logger.info(f'{title}: {edition_title}')
    else:
        logger.info(f'{title}: Cleared edition information')
    
    return True

# Process new movie
def process_new_movie(server, token, metadata, modules, excluded_languages):
    headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
    response = requests.get(f'{server}{metadata["key"]}', headers=headers)
    data = response.json()

    media_parts = data['MediaContainer']['Metadata'][0]['Media'][0]['Part']
    if media_parts:
        max_size_part = max(media_parts, key=lambda part: part['size'])
        file_path = max_size_part['file']
        file_name = os.path.basename(file_path)
        tags = []
        for module in modules:
            if module == 'Resolution':
                Resolution = get_Resolution(data['MediaContainer']['Metadata'][0])
                if Resolution:
                    tags.append(Resolution)
            elif module == 'Duration':
                Duration = get_Duration(data['MediaContainer']['Metadata'][0])
                if Duration:
                    tags.append(Duration)
            elif module == 'Rating':
                Rating = get_Rating(data['MediaContainer']['Metadata'][0], server, token, metadata['ratingKey'])
                if Rating:
                    tags.append(Rating)
                else:
                    logger.info(f"No rating found for new movie: {metadata.get('title', 'Unknown Title')}")
            elif module == 'Cut':
                Cut = get_Cut(file_name, server, token, metadata['ratingKey'])
                if Cut:
                    tags.append(Cut)
            elif module == 'Release':
                Release = get_Release(file_name, server, token, metadata['ratingKey'])
                if Release:
                    tags.append(Release)
            elif module == 'DynamicRange':
                DynamicRange = get_DynamicRange(server, token, metadata['ratingKey'])
                if DynamicRange:
                    tags.append(DynamicRange)
            elif module == 'Country':
                Country = get_Country(server, token, metadata['ratingKey'])
                if Country:
                    tags.append(Country)
            elif module == 'ContentRating':
                ContentRating = get_ContentRating(data['MediaContainer']['Metadata'][0])
                if ContentRating:
                    tags.append(ContentRating)
            elif module == 'Language':
                Language = get_Language(server, token, metadata['ratingKey'], excluded_languages)
                if Language:
                    tags.append(Language)
            elif module == 'AudioChannels':
                AudioChannels = get_AudioChannels(data['MediaContainer']['Metadata'][0])
                if AudioChannels:
                    tags.append(AudioChannels)
            elif module == 'Director':
                Director = get_Director(data['MediaContainer']['Metadata'][0])
                if Director:
                    tags.append(Director)
            elif module == 'Genre':
                Genre = get_Genre(data['MediaContainer']['Metadata'][0])
                if Genre:
                    tags.append(Genre)
            elif module == 'SpecialFeatures':
                SpecialFeatures = get_SpecialFeatures(data['MediaContainer']['Metadata'][0])
                if SpecialFeatures:
                    tags.append(SpecialFeatures)
            elif module == 'Studio':
                Studio = get_Studio(data['MediaContainer']['Metadata'][0])
                if Studio:
                    tags.append(Studio)
            elif module == 'AudioCodec':
                AudioCodec = get_AudioCodec(server, token, metadata['ratingKey'])
                if AudioCodec:
                    tags.append(AudioCodec)
            elif module == 'Bitrate':
                Bitrate = get_Bitrate(server, token, metadata['ratingKey'])
                if Bitrate:
                    tags.append(Bitrate)
            elif module == 'FrameRate':
                FrameRate = get_FrameRate(data['MediaContainer']['Metadata'][0])
                if FrameRate:
                    tags.append(FrameRate)
            elif module == 'Size':
                Size = get_Size(server, token, metadata['ratingKey'])
                if Size:
                    tags.append(Size)
            elif module == 'Source':
                Source = get_Source(file_name, server, token, metadata['ratingKey'])
                if Source:
                    tags.append(Source)
            elif module == 'VideoCodec':
                VideoCodec = get_VideoCodec(data['MediaContainer']['Metadata'][0])
                if VideoCodec:
                    tags.append(VideoCodec)
        update_movie(server, token, metadata, tags, modules)

# Reset movies with multi-threading
def reset_movies(server, token, skip_libraries, max_workers, batch_size):
    headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
    libraries = cached_request(f'{server}/library/sections', headers)['MediaContainer']['Directory']
    
    # Collect all movies that need to be reset
    all_to_reset = []
    library_info = {}
    
    for library in libraries:
        if library['type'] == 'movie' and library['title'] not in skip_libraries:
            library_key = library['key']
            lib_title = library['title']
            
            response = cached_request(f'{server}/library/sections/{library_key}/all', headers)
            if 'MediaContainer' in response and 'Metadata' in response['MediaContainer']:
                library_movies = response['MediaContainer']['Metadata']
                # Only include movies with editionTitle
                to_reset = [m for m in library_movies if 'editionTitle' in m]
                all_to_reset.extend(to_reset)
                library_info[lib_title] = len(to_reset)
    
    logger.info(f"Total movies to reset: {len(all_to_reset)}")
    for lib_title, count in library_info.items():
        logger.info(f'Library: {lib_title}, Movies to reset: {count}')
    
    # Process in batches with ThreadPoolExecutor
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for i in range(0, len(all_to_reset), batch_size):
            batch = all_to_reset[i:i+batch_size]
            # Process each movie in the batch
            for movie in batch:
                executor.submit(reset_movie, server, token, movie)
            logger.info(f"Submitted reset batch {i//batch_size + 1}/{(len(all_to_reset)+batch_size-1)//batch_size}")

# Reset a single movie
def reset_movie(server, token, movie):
    movie_id = movie['ratingKey']
    title = movie.get('title', 'Unknown')
    
    try:
        params = {'type': 1, 'id': movie_id, 'editionTitle.value': '', 'editionTitle.locked': 0}
        session = get_session()
        session.put(f'{server}/library/metadata/{movie_id}', headers={'X-Plex-Token': token}, params=params)
        logger.info(f'Reset {title}')
        return True
    except Exception as e:
        logger.error(f"Error resetting movie {title}: {str(e)}")
        return False

# Backup metadata
def backup_metadata(server, token, backup_file):
    headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
    libraries = requests.get(f'{server}/library/sections', headers=headers).json()['MediaContainer']['Directory']
    
    metadata = {}
    for library in libraries:
        if library['type'] == 'movie':
            library_key = library['key']
            response = requests.get(f'{server}/library/sections/{library_key}/all', headers=headers).json()
            if 'MediaContainer' in response and 'Metadata' in response['MediaContainer']:
                for movie in response['MediaContainer']['Metadata']:
                    metadata[movie['ratingKey']] = {
                        'title': movie['title'],
                        'editionTitle': movie.get('editionTitle', '')
                    }
    
    os.makedirs(os.path.dirname(backup_file), exist_ok=True)
    
    with open(backup_file, 'w') as f:
        json.dump(metadata, f, indent=2)

# Restore metadata
def restore_metadata(server, token, backup_file):
    with open(backup_file, 'r') as f:
        metadata = json.load(f)
    
    headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
    for movie_id, movie_data in metadata.items():
        if movie_data['editionTitle']:
            params = {
                'type': 1,
                'id': movie_id,
                'editionTitle.value': movie_data['editionTitle'],
                'editionTitle.locked': 1
            }
            requests.put(f'{server}/library/metadata/{movie_id}', headers=headers, params=params)

# Main function
def main():
    server, token, skip_libraries, modules, excluded_languages, max_workers, batch_size = initialize_settings()
    
    parser = argparse.ArgumentParser(description='Manage Plex server movie editions')
    parser.add_argument('--all', action='store_true', help='Add edition info to all movies')
    parser.add_argument('--new', action='store_true', help='Add edition info to new movies')
    parser.add_argument('--reset', action='store_true', help='Reset edition info for all movies')
    parser.add_argument('--backup', action='store_true', help='Backup movie metadata')
    parser.add_argument('--restore', action='store_true', help='Restore movie metadata from backup')
    parser.add_argument('--clear-cache', action='store_true', help='Clear cached data')
    
    args = parser.parse_args()
    
    if args.clear_cache:
        logger.info("Clearing cache...")
        cache.clear()
        logger.info("Cache cleared.")
    
    backup_file = Path(__file__).parent / 'metadata_backup' / 'metadata_backup.json'
    
    if args.backup:
        backup_metadata(server, token, backup_file)
        logger.info('Metadata backup completed.')
    elif args.restore:
        restore_metadata(server, token, backup_file)
        logger.info('Metadata restoration completed.')
    elif args.all:
        process_movies(server, token, skip_libraries, modules, excluded_languages, max_workers, batch_size)
    elif args.new:
        app = Flask(__name__)
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

        @app.route('/', methods=['POST'])
        def webhook():
            file = request.files.get('thumb')
            payload = request.form.get('payload')
            if payload:
                data = json.loads(payload)
                event = data.get('event')
                if event == 'library.new':
                    metadata = data.get('Metadata')
                    library = metadata.get('librarySectionTitle')
                    if library not in skip_libraries:
                        if metadata and metadata.get('type') == 'movie':
                            process_new_movie(server, token, metadata, modules, excluded_languages)
            return 'OK', 200

        logger.info('Starting webhook server for processing new movies...')
        app.run(host='0.0.0.0', port=8089)
    elif args.reset:
        reset_movies(server, token, skip_libraries, max_workers, batch_size)
    else:
        logger.info('No action specified. Please use one of the following arguments:')
        logger.info('  --all: Add edition info to all movies')
        logger.info('  --new: Start webhook server to add edition info to new movies')
        logger.info('  --reset: Reset edition info for all movies')
        logger.info('  --backup: Backup movie metadata')
        logger.info('  --restore: Restore movie metadata from backup')
        logger.info('  --clear-cache: Clear cached data')
    
    try:
        cache_stats = cache.stats()
        if isinstance(cache_stats, dict):
            hits = cache_stats.get('hits', 0)
            misses = cache_stats.get('misses', 0)
        else:
            hits = cache_stats[0] if len(cache_stats) > 0 else 0
            misses = cache_stats[1] if len(cache_stats) > 1 else 0
            
        cache_size_mb = cache.volume() // (1024 * 1024) if hasattr(cache, 'volume') else 0
        logger.info(f"Cache statistics: hits={hits}, misses={misses}, size={cache_size_mb}MB")
    except Exception as e:
        logger.info(f"Unable to get cache statistics: {str(e)}")

    logger.info('Script execution completed.')

if __name__ == '__main__':
    main()
