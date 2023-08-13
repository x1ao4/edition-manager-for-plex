import os
import re
import json
from getpass import getpass
from plexapi.myplex import MyPlexAccount

# 读取配置文件
def read_config():
    if os.path.exists('config.json'):
        with open('config.json', 'r') as f:
            config = json.load(f)
            return config['username'], config['password'], config['server_name']
    else:
        return None, None, None

# 写入配置文件
def write_config(username, password, server_name):
    with open('config.json', 'w') as f:
        json.dump({'username': username, 'password': password, 'server_name': server_name}, f)

# 获取用户名、密码和服务器名称
def get_credentials():
    username, password, server_name = read_config()
    if not username or not password or not server_name:
        username = input('Please enter your Plex username: ')
        password = getpass('Please enter your Plex password: ')
        server_name = input('Please enter your Plex server name: ')
        print()
        write_config(username, password, server_name)
    return username, password, server_name

# 获取所有电影
def get_movies(server):
    movies = []
    for library in server.library.sections():
        if library.type == 'movie':
            movies.extend(library.all())
    return movies

# 判断版本
def get_edition(filename):
    filename = filename.upper()
    if re.search(r'\bREMUX\b', filename):
        edition = 'REMUX'
    elif re.search(r'\b(BLURAY|BD|BLU-RAY)\b', filename):
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
    elif re.search(r'\bTC\b', filename):
        edition = 'TC'
    elif re.search(r'\b(HQCAM|HQ-CAM)\b', filename):
        edition = 'HQCAM'
    elif re.search(r'\bCAM\b', filename):
        edition = 'CAM'
    elif re.search(r'\bTS\b', filename):
        edition = 'TS'
    else:
        edition = None

    if edition and (re.search(r'\bDOVI\b', filename) or re.search(r'\bDV\b', filename)):
        edition += ' · DV'

    return edition

# 更新电影信息
def update_movie(movie, edition):
    existing_edition = movie.editionTitle
    if not existing_edition and edition:
        movie.editEditionTitle(edition)
        print(f'Updated Edition for movie \"{movie.title}\" to {edition}')
        return True
    else:
        return False

def main():
    # 获取用户名、密码和服务器名称
    username, password, server_name = get_credentials()

    # 登录 Plex 账号并选择服务器
    account = MyPlexAccount(username, password)
    server = account.resource(server_name).connect()

    # 获取所有电影并更新信息
    movies = get_movies(server)
    count = 0
    for movie in movies:
        media_parts = movie.media[0].parts
        if media_parts and media_parts[0].file:
            file_path = media_parts[0].file
            file_name = os.path.basename(file_path)
            edition = get_edition(file_name)
            if update_movie(movie, edition):
                count += 1

    print()
    print(f'Total updated: {count}')

if __name__ == '__main__':
    main()
