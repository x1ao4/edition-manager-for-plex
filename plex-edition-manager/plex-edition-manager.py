import os
import re
import requests
from configparser import ConfigParser

# 读取配置文件
def read_config():
    config = ConfigParser()
    config.read('config.ini')
    if 'server' in config.sections():
        server = config.get('server', 'address')
        token = config.get('server', 'token')
        return server, token
    else:
        return None, None

# 写入配置文件
def write_config(server, token):
    config = ConfigParser()
    config.add_section('server')
    config.set('server', 'address', server)
    config.set('server', 'token', token)
    with open('config.ini', 'w') as f:
        config.write(f)

# 获取服务器地址和令牌
def get_credentials():
    server, token = read_config()
    if not server or not token:
        server = input('Please enter your Plex server address: ')
        token = input('Please enter your Plex token: ')
        print()
        write_config(server, token)
    return server, token

# 获取所有电影
def get_movies(server, token):
    movies = []
    headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
    libraries = requests.get(f'{server}/library/sections', headers=headers).json()['MediaContainer']['Directory']
    for library in libraries:
        if library['type'] == 'movie':
            library_key = library['key']
            library_movies = requests.get(f'{server}/library/sections/{library_key}/all', headers=headers).json()['MediaContainer']['Metadata']
            movies.extend(library_movies)
    return movies

# 判断版本
def get_edition(filename):
    filename = filename.upper()
    if re.search(r'\b(REMUX|BDREMUX|BD-REMUX)\b', filename):
        edition = 'REMUX'
    elif re.search(r'\b(BLURAY|BD|BLU-RAY|BD1080P)\b', filename):
        edition = 'BD'
    elif re.search(r'\bBDRIP\b', filename):
        edition = 'BDRIP'
    elif re.search(r'\bWEB-DL|WEBDL\b', filename):
        edition = 'WEB-DL'
    elif re.search(r'\bWEBRIP\b', filename):
        edition = 'WEBRIP'
    elif re.search(r'\bHR-HDTV|HRHDTV\b', filename):
        edition = 'HR-HDTV'
    elif re.search(r'\bHDTV\b', filename):
        edition = 'HDTV'
    elif re.search(r'\bHDRIP\b', filename):
        edition = 'HDRIP'
    elif re.search(r'\bDVDRIP\b', filename):
        edition = 'DVDRIP'
    elif re.search(r'\bDVDSCR\b', filename):
        edition = 'DVDSCR'
    elif re.search(r'\bDVD\b', filename):
        edition = 'DVD'
    elif re.search(r'\bHDTC\b', filename):
        edition = 'HDTC'
    elif re.search(r'\bTC\b', filename) and not filename.endswith('.TC'):
        edition = 'TC'
    elif re.search(r'\b(HQCAM|HQ-CAM)\b', filename):
        edition = 'HQCAM'
    elif re.search(r'\bCAM\b', filename):
        edition = 'CAM'
    elif re.search(r'\bTS\b', filename) and not filename.endswith('.TS'):
        edition = 'TS'
    else:
        edition = None

    if edition and (re.search(r'\bDOVI\b', filename) or re.search(r'\bDV\b', filename)):
        edition += ' · DV'

    return edition

# 更新电影信息
def update_movie(server, token, movie, edition):
	# 通过existing_edition获取项目是否存在editionTitle
	existing_edition = movie.get('editionTitle')

	# 如果不存在editionTitle，则更新版本信息并打印信息
	if not existing_edition and edition:
		movie_id = movie['ratingKey']
		params = {'type': 1, 'id': movie_id, 'editionTitle.value': edition, 'editionTitle.locked': 1}
		requests.put(f'{server}/library/metadata/{movie_id}', headers={'X-Plex-Token': token}, params=params)
		print(f'Updated Edition for movie \"{movie["title"]}\" to {edition}')
		return True
	else:
		return False

def main():
	# 获取服务器地址和令牌
	server, token = get_credentials()

	# 获取所有电影并更新信息
	movies = get_movies(server, token)
	count = 0
	for movie in movies:
		media_parts = movie['Media'][0]['Part']
		if media_parts and media_parts[0]['file']:
			file_path = media_parts[0]['file']
			file_name = os.path.basename(file_path)
			edition = get_edition(file_name)
			if update_movie(server, token, movie, edition):
				count += 1

	print()
	print(f'Total updated: {count}')

if __name__ == '__main__':
	main()
