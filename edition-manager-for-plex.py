import os
import re
import sys
import time
import json
import logging
import requests
import argparse
from modules.Cut import get_Cut
from modules.Size import get_Size
from modules.Source import get_Source
from modules.Rating import get_Rating
from modules.Bitrate import get_Bitrate
from modules.Country import get_Country
from modules.Release import get_Release
from modules.Duration import get_Duration
from modules.FrameRate import get_FrameRate
from modules.AudioCodec import get_AudioCodec
from modules.VideoCodec import get_VideoCodec
from modules.Resolution import get_Resolution
from modules.DynamicRange import get_DynamicRange
from modules.ContentRating import get_ContentRating
from pathlib import Path
from flask import Flask, request
from configparser import ConfigParser

# 创建一个日志记录器
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('[%(asctime)s] %(message)s', datefmt='%Y-%m-%d %H:%M:%S')
handler.setFormatter(formatter)
logger.addHandler(handler)

# 初始化设置
def initialize_settings():
    config_file = Path(__file__).parent / 'config' / 'config.ini'
    config = ConfigParser()
    config.read(config_file)
    if 'server' in config.sections():
        server = config.get('server', 'address')
        token = config.get('server', 'token')
        skip_libraries = set(re.split(r'[；;]', config.get('server', 'skip_libraries'))) if config.has_option('server', 'skip_libraries') else set()
        language = config.get('server', 'language') if config.has_option('server', 'language') else 'en'
        module_mapping = {'片源版本': 'Source', '分辨率': 'Resolution', '音频编码': 'AudioCodec', '视频编码': 'VideoCodec', '帧率': 'FrameRate', '比特率': 'Bitrate', '时长': 'Duration', '评分': 'Rating', '剪辑版本': 'Cut', '发行版本': 'Release', '动态范围': 'DynamicRange', '国家': 'Country', '内容分级': 'ContentRating', '大小': 'Size'}
        modules = re.split(r'[；;]', config.get('modules', 'order')) if config.has_option('modules', 'order') else ['Source', 'Resolution', 'AudioCodec', 'VideoCodec', 'FrameRate', 'Bitrate', 'Duration', 'Rating', 'Cut', 'Release', 'DynamicRange', 'Country', 'ContentRating', 'Size']
        modules = [module_mapping.get(module, module) for module in modules]
        try:
            headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
            response = requests.get(server, headers=headers)
            response.raise_for_status()
            server_name = response.json()['MediaContainer']['friendlyName']
            if language == 'zh':
                logger.info(f"已成功连接到服务器：{server_name}")
            else:
                logger.info(f"Successfully connected to server: {server_name}")
        except requests.exceptions.RequestException as err:
            if language == 'zh':
                logger.error("服务器连接失败，请检查配置文件或网络的设置是否有误。如需帮助，请访问 https://github.com/x1ao4/edition-manager-for-plex 查看使用说明。\n")
            else:
                logger.error("Server connection failed, please check the settings in the configuration file or your network. For help, please visit https://github.com/x1ao4/edition-manager-for-plex for instructions. \n")
            time.sleep(10)
            raise SystemExit(err)
        return server, token, skip_libraries, language, modules

# 获取并处理所有电影
def process_movies(server, token, skip_libraries, language, modules):
    headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
    libraries = requests.get(f'{server}/library/sections', headers=headers).json()['MediaContainer']['Directory']
    for library in libraries:
        if library['type'] == 'movie' and library['title'] not in skip_libraries:
            library_key = library['key']
            response = requests.get(f'{server}/library/sections/{library_key}/all', headers=headers).json()
            if 'MediaContainer' in response and 'Metadata' in response['MediaContainer']:
                library_movies = response['MediaContainer']['Metadata']
                logger.info(f'')
                if language == 'zh':
                    logger.info(f'处理库：{library["title"]}')
                    logger.info(f'电影数：{len(library_movies)}')
                else:
                    logger.info(f'Processing library: {library["title"]}')
                    logger.info(f'Movie count: {len(library_movies)}')
                for movie in library_movies:
                    media_parts = movie['Media'][0]['Part']
                    if media_parts:
                        # 找到文件大小最大的视频文件
                        max_size_part = max(media_parts, key=lambda part: part['size'])
                        file_path = max_size_part['file']
                        file_name = os.path.basename(file_path)
                        tags = []
                        for module in modules:
                            if module == 'Source':
                                Source = get_Source(file_name, server, token, movie['ratingKey'])
                                if Source:
                                    tags.append(Source)
                            elif module == 'Resolution':
                                Resolution = get_Resolution(movie)
                                if Resolution:
                                    tags.append(Resolution)
                            elif module == 'AudioCodec':
                                AudioCodec = get_AudioCodec(server, token, movie['ratingKey'], language)
                                if AudioCodec:
                                    tags.append(AudioCodec)
                            elif module == 'VideoCodec':
                                VideoCodec = get_VideoCodec(movie)
                                if VideoCodec:
                                    tags.append(VideoCodec)
                            elif module == 'FrameRate':
                                FrameRate = get_FrameRate(movie)
                                if FrameRate:
                                    tags.append(FrameRate)
                            elif module == 'Bitrate':
                                Bitrate = get_Bitrate(server, token, movie['ratingKey'])
                                if Bitrate:
                                    tags.append(Bitrate)
                            elif module == 'Duration':
                                Duration = get_Duration(movie, language)
                                if Duration:
                                    tags.append(Duration)
                            elif module == 'Rating':
                                Rating = get_Rating(movie)
                                if Rating:
                                    tags.append(Rating)
                            elif module == 'Cut':
                                Cut = get_Cut(file_name, server, token, movie['ratingKey'], language)
                                if Cut:
                                    tags.append(Cut)
                            elif module == 'Release':
                                Release = get_Release(file_name, server, token, movie['ratingKey'], language)
                                if Release:
                                    tags.append(Release)
                            elif module == 'DynamicRange':
                                DynamicRange = get_DynamicRange(server, token, movie['ratingKey'])
                                if DynamicRange:
                                    tags.append(DynamicRange)
                            elif module == 'Country':
                                Country = get_Country(server, token, movie['ratingKey'], language)
                                if Country:
                                    tags.append(Country)
                            elif module == 'ContentRating':
                                ContentRating = get_ContentRating(movie)
                                if ContentRating:
                                    tags.append(ContentRating)
                            elif module == 'Size':
                                Size = get_Size(server, token, movie['ratingKey'])
                                if Size:
                                    tags.append(Size)
                        update_movie(server, token, movie, tags, language)

# 更新版本信息
def update_movie(server, token, movie, tags, language):
    # 通过 existing_edition 判断电影是否存在 editionTitle
    existing_edition = movie.get('editionTitle')

    # 如果不存在 editionTitle，并且 tags 不为空，则更新版本信息并打印信息
    if not existing_edition and tags:
        movie_id = movie['ratingKey']
        edition_title = ' · '.join(tags)
        params = {'type': 1, 'id': movie_id, 'editionTitle.value': edition_title, 'editionTitle.locked': 1}
        requests.put(f'{server}/library/metadata/{movie_id}', headers={'X-Plex-Token': token}, params=params)
        if language == 'zh':
            logger.info(f'{movie["title"]}：{edition_title}')
        else:
            logger.info(f'{movie["title"]}: {edition_title}')
        return True
    else:
        return False

# 处理新增电影
def process_new_movie(server, token, metadata, language, modules):
    # 获取新增电影的详细信息
    headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
    response = requests.get(f'{server}{metadata["key"]}', headers=headers)
    data = response.json()

    # 提取文件的路径和名称
    media_parts = data['MediaContainer']['Metadata'][0]['Media'][0]['Part']
    if media_parts:
        # 找到文件大小最大的视频文件
        max_size_part = max(media_parts, key=lambda part: part['size'])
        file_path = max_size_part['file']
        file_name = os.path.basename(file_path)
        tags = []
        for module in modules:
            if module == 'Source':
                Source = get_Source(file_name, server, token, metadata['ratingKey'])
                if Source:
                    tags.append(Source)
            elif module == 'Resolution':
                Resolution = get_Resolution(data['MediaContainer']['Metadata'][0])
                if Resolution:
                    tags.append(Resolution)
            elif module == 'AudioCodec':
                AudioCodec = get_AudioCodec(server, token, metadata['ratingKey'], language)
                if AudioCodec:
                    tags.append(AudioCodec)
            elif module == 'VideoCodec':
                VideoCodec = get_VideoCodec(data['MediaContainer']['Metadata'][0])
                if VideoCodec:
                    tags.append(VideoCodec)
            elif module == 'FrameRate':
                FrameRate = get_FrameRate(data['MediaContainer']['Metadata'][0])
                if FrameRate:
                    tags.append(FrameRate)
            elif module == 'Bitrate':
                Bitrate = get_Bitrate(server, token, metadata['ratingKey'])
                if Bitrate:
                    tags.append(Bitrate)
            elif module == 'Duration':
                Duration = get_Duration(data['MediaContainer']['Metadata'][0], language)
                if Duration:
                    tags.append(Duration)
            elif module == 'Rating':
                Rating = get_Rating(data['MediaContainer']['Metadata'][0])
                if Rating:
                    tags.append(Rating)
            elif module == 'Cut':
                Cut = get_Cut(file_name, server, token, metadata['ratingKey'], language)
                if Cut:
                    tags.append(Cut)
            elif module == 'Release':
                Release = get_Release(file_name, server, token, metadata['ratingKey'], language)
                if Release:
                    tags.append(Release)
            elif module == 'DynamicRange':
                DynamicRange = get_DynamicRange(server, token, metadata['ratingKey'])
                if DynamicRange:
                    tags.append(DynamicRange)
            elif module == 'Country':
                Country = get_Country(server, token, metadata['ratingKey'], language)
                if Country:
                    tags.append(Country)
            elif module == 'ContentRating':
                ContentRating = get_ContentRating(data['MediaContainer']['Metadata'][0])
                if ContentRating:
                    tags.append(ContentRating)
            elif module == 'Size':
                Size = get_Size(server, token, metadata['ratingKey'])
                if Size:
                    tags.append(Size)
        update_movie(server, token, metadata, tags, language)

# 重置电影的版本信息
def reset_movie(server, token, movie, language):
    # 通过 existing_edition 判断电影是否存在 editionTitle
    existing_edition = movie.get('editionTitle')

    # 如果存在 editionTitle，则重置版本信息并打印信息
    if existing_edition:
        movie_id = movie['ratingKey']
        params = {'type': 1, 'id': movie_id, 'editionTitle.value': '', 'editionTitle.locked': 0}
        requests.put(f'{server}/library/metadata/{movie_id}', headers={'X-Plex-Token': token}, params=params)
        if language == 'zh':
            logger.info(f'已重置{movie["title"]}')
        else:
            logger.info(f'Reset {movie["title"]}')
        return True
    else:
        return False

# 重置所有电影的版本信息
def reset_movies(server, token, skip_libraries, language):
    headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
    libraries = requests.get(f'{server}/library/sections', headers=headers).json()['MediaContainer']['Directory']
    for library in libraries:
        if library['type'] == 'movie' and library['title'] not in skip_libraries:
            library_key = library['key']
            response = requests.get(f'{server}/library/sections/{library_key}/all', headers=headers).json()
            if 'MediaContainer' in response and 'Metadata' in response['MediaContainer']:
                library_movies = response['MediaContainer']['Metadata']
                logger.info(f'')
                if language == 'zh':
                    logger.info(f'重置库：{library["title"]}')
                    logger.info(f'电影数：{len(library_movies)}')
                else:
                    logger.info(f'Resetting library: {library["title"]}')
                    logger.info(f'Movie count: {len(library_movies)}')
                for movie in library_movies:
                    reset_movie(server, token, movie, language)

def main():
    # 创建一个解析器
    parser = argparse.ArgumentParser(description='管理 Plex 服务器上的电影的版本信息')
    # 添加选项，用户可以通过这些选项来选择运行哪个功能
    parser.add_argument('--all', action='store_true', help='为所有电影添加版本信息')
    parser.add_argument('--new', action='store_true', help='为新增电影添加版本信息')
    parser.add_argument('--reset', action='store_true', help='为所有电影重置版本信息')

    args = parser.parse_args()

    # 获取服务器地址和令牌
    server, token, skip_libraries, language, modules = initialize_settings()

    if args.all:
        # 获取并处理所有电影
        process_movies(server, token, skip_libraries, language, modules)
    elif args.new:
        app = Flask(__name__)
        log = logging.getLogger('werkzeug')
        log.setLevel(logging.ERROR)

        # 定义 webhook 路由
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
                            process_new_movie(server, token, metadata, language, modules)
            return 'OK', 200

        # 启动 Flask 服务器
        app.run(host='0.0.0.0', port=8089)
    elif args.reset:
        # 重置所有电影的版本信息
        reset_movies(server, token, skip_libraries, language)

    logger.info('')

if __name__ == '__main__':
    main()
