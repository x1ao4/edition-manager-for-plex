import os
import re
import sys
import time
import json
import logging
import requests
import argparse
from modules.Cut import get_Cut
from modules.Rating import get_Rating
from modules.Country import get_Country
from modules.Release import get_Release
from modules.Duration import get_Duration
from modules.Resolution import get_Resolution
from modules.DynamicRange import get_DynamicRange
from modules.ContentRating import get_ContentRating
from modules.Language import get_Language
from modules.AudioChannels import get_AudioChannels
from modules.Director import get_Director
from modules.Genre import get_Genre
from modules.SpecialFeatures import get_SpecialFeatures
from modules.Studio import get_Studio
from pathlib import Path
from flask import Flask, request
from configparser import ConfigParser

# Create a logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Initialize settings
def initialize_settings():
    config_file = Path(__file__).parent / 'config' / 'config.ini'
    config = ConfigParser()
    config.read(config_file)
    if 'server' in config.sections():
        server = config.get('server', 'address')
        token = config.get('server', 'token')
        skip_libraries = set(re.split(r'[；;]', config.get('server', 'skip_libraries'))) if config.has_option('server', 'skip_libraries') else set()
        modules = re.split(r'[；;]', config.get('modules', 'order')) if config.has_option('modules', 'order') else ['Resolution', 'Duration', 'Rating', 'Cut', 'Release', 'DynamicRange', 'Country', 'ContentRating', 'Language']
        
        excluded_languages = set()
        if config.has_option('language', 'excluded_languages'):
            excluded_languages = set(lang.strip() for lang in re.split(r'[,;]', config.get('language', 'excluded_languages')))
        
        try:
            headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
            response = requests.get(server, headers=headers)
            response.raise_for_status()
            server_name = response.json()['MediaContainer']['friendlyName']
            logger.info(f"Successfully connected to server: {server_name}")
        except requests.exceptions.RequestException as err:
            logger.error("Server connection failed, please check the settings in the configuration file or your network. For help, please visit https://github.com/x1ao4/edition-manager-for-plex for instructions.")
            time.sleep(10)
            raise SystemExit(err)
        return server, token, skip_libraries, modules, excluded_languages

# Process all movies
def process_movies(server, token, skip_libraries, modules, excluded_languages):
    headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
    libraries = requests.get(f'{server}/library/sections', headers=headers).json()['MediaContainer']['Directory']
    for library in libraries:
        if library['type'] == 'movie' and library['title'] not in skip_libraries:
            library_key = library['key']
            response = requests.get(f'{server}/library/sections/{library_key}/all', headers=headers).json()
            if 'MediaContainer' in response and 'Metadata' in response['MediaContainer']:
                library_movies = response['MediaContainer']['Metadata']
                logger.info(f'')
                logger.info(f'Processing library: {library["title"]}')
                logger.info(f'Movie count: {len(library_movies)}')
                for movie in library_movies:
                    process_single_movie(server, token, movie, modules, excluded_languages)

def process_single_movie(server, token, movie, modules, excluded_languages):
    media_parts = movie['Media'][0]['Part']
    if media_parts:
        max_size_part = max(media_parts, key=lambda part: part['size'])
        file_path = max_size_part['file']
        file_name = os.path.basename(file_path)
        tags = []
        
        for module in modules:
            if module == 'Resolution':
                Resolution = get_Resolution(movie)
                if Resolution:
                    tags.append(Resolution)
            elif module == 'Duration':
                Duration = get_Duration(movie)
                if Duration:
                    tags.append(Duration)
            elif module == 'Rating':
                Rating = get_Rating(movie, server, token, movie['ratingKey'])
                if Rating:
                    tags.append(Rating)
            elif module == 'Cut':
                Cut = get_Cut(file_name, server, token, movie['ratingKey'])
                if Cut:
                    tags.append(Cut)
            elif module == 'Release':
                Release = get_Release(file_name, server, token, movie['ratingKey'])
                if Release:
                    tags.append(Release)
            elif module == 'DynamicRange':
                DynamicRange = get_DynamicRange(server, token, movie['ratingKey'])
                if DynamicRange:
                    tags.append(DynamicRange)
            elif module == 'Country':
                Country = get_Country(server, token, movie['ratingKey'])
                if Country:
                    tags.append(Country)
            elif module == 'ContentRating':
                ContentRating = get_ContentRating(movie)
                if ContentRating:
                    tags.append(ContentRating)
            elif module == 'Language':
                Language = get_Language(server, token, movie['ratingKey'], excluded_languages)
                if Language:
                    tags.append(Language)
            elif module == 'AudioChannels':
                AudioChannels = get_AudioChannels(movie)
                if AudioChannels:
                    tags.append(AudioChannels)
            elif module == 'Director':
                Director = get_Director(movie)
                if Director:
                    tags.append(Director)
            elif module == 'Genre':
                Genre = get_Genre(movie)
                if Genre:
                    tags.append(Genre)
            elif module == 'SpecialFeatures':
                SpecialFeatures = get_SpecialFeatures(movie)
                if SpecialFeatures:
                    tags.append(SpecialFeatures)
            elif module == 'Studio':
                Studio = get_Studio(movie)
                if Studio:
                    tags.append(Studio)
        
        # Always call update_movie, even if tags is empty
        update_movie(server, token, movie, tags, modules)

def update_movie(server, token, movie, tags, modules):
    movie_id = movie['ratingKey']
    
    # Clear existing edition title and rating
    clear_params = {
        'type': 1,
        'id': movie_id,
        'editionTitle.value': '',
        'editionTitle.locked': 0,
        'rating.value': '',
        'rating.locked': 0
    }
    requests.put(f'{server}/library/metadata/{movie_id}', headers={'X-Plex-Token': token}, params=clear_params)
    
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
        
        requests.put(f'{server}/library/metadata/{movie_id}', headers={'X-Plex-Token': token}, params=params)
        logger.info(f'{movie["title"]}: {edition_title}')
    else:
        logger.info(f'{movie["title"]}: Cleared edition information')
    
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
        update_movie(server, token, metadata, tags)

# Reset movie edition information
def reset_movie(server, token, movie):
    existing_edition = movie.get('editionTitle')

    if existing_edition:
        movie_id = movie['ratingKey']
        params = {'type': 1, 'id': movie_id, 'editionTitle.value': '', 'editionTitle.locked': 0}
        requests.put(f'{server}/library/metadata/{movie_id}', headers={'X-Plex-Token': token}, params=params)
        logger.info(f'Reset {movie["title"]}')
        return True
    else:
        return False

# Reset all movies' edition information
def reset_movies(server, token, skip_libraries):
    headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
    libraries = requests.get(f'{server}/library/sections', headers=headers).json()['MediaContainer']['Directory']
    for library in libraries:
        if library['type'] == 'movie' and library['title'] not in skip_libraries:
            library_key = library['key']
            response = requests.get(f'{server}/library/sections/{library_key}/all', headers=headers).json()
            if 'MediaContainer' in response and 'Metadata' in response['MediaContainer']:
                library_movies = response['MediaContainer']['Metadata']
                logger.info(f'')
                logger.info(f'Resetting library: {library["title"]}')
                logger.info(f'Movie count: {len(library_movies)}')
                for movie in library_movies:
                    reset_movie(server, token, movie)

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

def main():
    server, token, skip_libraries, modules, excluded_languages = initialize_settings()
    
    parser = argparse.ArgumentParser(description='Manage Plex server movie editions')
    parser.add_argument('--all', action='store_true', help='Add edition info to all movies')
    parser.add_argument('--new', action='store_true', help='Add edition info to new movies')
    parser.add_argument('--reset', action='store_true', help='Reset edition info for all movies')
    parser.add_argument('--backup', action='store_true', help='Backup movie metadata')
    parser.add_argument('--restore', action='store_true', help='Restore movie metadata from backup')
    
    args = parser.parse_args()
    
    backup_file = Path(__file__).parent / 'metadata_backup' / 'metadata_backup.json'
    
    if args.backup:
        backup_metadata(server, token, backup_file)
        logger.info('Metadata backup completed.')
    elif args.restore:
        restore_metadata(server, token, backup_file)
        logger.info('Metadata restoration completed.')
    elif args.all:
        process_movies(server, token, skip_libraries, modules, excluded_languages)
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
        reset_movies(server, token, skip_libraries)
    else:
        logger.info('No action specified. Please use one of the following arguments:')
        logger.info('  --all: Add edition info to all movies')
        logger.info('  --new: Start webhook server to add edition info to new movies')
        logger.info('  --reset: Reset edition info for all movies')
        logger.info('  --backup: Backup movie metadata')
        logger.info('  --restore: Restore movie metadata from backup')
    
    logger.info('Script execution completed.')

if __name__ == '__main__':
    main()
