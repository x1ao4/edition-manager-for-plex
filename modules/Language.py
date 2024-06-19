import requests

def get_Language(server, token, movie_id):
    headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
    response = requests.get(f'{server}/library/metadata/{movie_id}', headers=headers)
    data = response.json()

    media = data['MediaContainer']['Metadata'][0]['Media'][0]['Part'][0]
    if 'Stream' in media:
        audio_streams = [stream for stream in media['Stream'] if stream['streamType'] == 2]

        # Skip processing if there are multiple audio tracks
        if len(audio_streams) > 1:
            return None

        # Mapping of common language codes to full names in alphabetical order
        language_mapping = {
            'af': 'Afrikaans',
            'am': 'Amharic',
            'ar': 'Arabic',
            'as': 'Assamese',
            'ay': 'Aymara',
            'az': 'Azerbaijani',
            'bh': 'Bihari',
            'bi': 'Bislama',
            'bn': 'Bengali',
            'bo': 'Tibetan',
            'bs': 'Bosnian',
            'bg': 'Bulgarian',
            'ca': 'Catalan',
            'cs': 'Czech',
            'cy': 'Welsh',
            'da': 'Danish',
            'de': 'German',
            'dz': 'Dzongkha',
            'el': 'Greek',
            'en': 'English',
            'es': 'Spanish',
            'et': 'Estonian',
            'eu': 'Basque',
            'fa': 'Persian',
            'fi': 'Finnish',
            'fj': 'Fijian',
            'fr': 'French',
            'ga': 'Irish',
            'gu': 'Gujarati',
            'he': 'Hebrew',
            'hi': 'Hindi',
            'hr': 'Croatian',
            'hu': 'Hungarian',
            'hy': 'Armenian',
            'id': 'Indonesian',
            'ig': 'Igbo',
            'is': 'Icelandic',
            'it': 'Italian',
            'iu': 'Inuktitut',
            'ja': 'Japanese',
            'jv': 'Javanese',
            'ka': 'Georgian',
            'kk': 'Kazakh',
            'km': 'Khmer',
            'kn': 'Kannada',
            'ko': 'Korean',
            'ks': 'Kashmiri',
            'ky': 'Kyrgyz',
            'lo': 'Lao',
            'lt': 'Lithuanian',
            'lv': 'Latvian',
            'mg': 'Malagasy',
            'mi': 'Maori',
            'mk': 'Macedonian',
            'ml': 'Malayalam',
            'mn': 'Mongolian',
            'mr': 'Marathi',
            'ms': 'Malay',
            'mt': 'Maltese',
            'my': 'Burmese',
            'ne': 'Nepali',
            'nl': 'Dutch',
            'no': 'Norwegian',
            'ny': 'Chichewa',
            'oj': 'Ojibwe',
            'om': 'Oromo',
            'or': 'Odia',
            'pa': 'Punjabi',
            'pl': 'Polish',
            'pt': 'Portuguese',
            'qu': 'Quechua',
            'ro': 'Romanian',
            'ru': 'Russian',
            'rw': 'Kinyarwanda',
            'si': 'Sinhala',
            'sk': 'Slovak',
            'sl': 'Slovenian',
            'sm': 'Samoan',
            'so': 'Somali',
            'sq': 'Albanian',
            'sr': 'Serbian',
            'ss': 'Swati',
            'st': 'Sotho',
            'su': 'Sundanese',
            'sv': 'Swedish',
            'sw': 'Swahili',
            'ta': 'Tamil',
            'te': 'Telugu',
            'th': 'Thai',
            'ti': 'Tigrinya',
            'tl': 'Tagalog',
            'tn': 'Tswana',
            'to': 'Tonga',
            'tr': 'Turkish',
            'ts': 'Tsonga',
            'tt': 'Tatar',
            'uk': 'Ukrainian',
            'ur': 'Urdu',
            'uz': 'Uzbek',
            've': 'Venda',
            'vi': 'Vietnamese',
            'xh': 'Xhosa',
            'yo': 'Yoruba',
            'zh': 'Chinese',
            'zu': 'Zulu',
            'nv': 'Navajo',
            'cr': 'Cree',
            'mh': 'Marshallese',
            'ho': 'Hiri Motu',
            'hz': 'Herero',
            'ty': 'Tahitian',
            'to': 'Tonga',
        }

        # Proceed only if there is a single audio track
        if len(audio_streams) == 1:
            language_code = audio_streams[0].get('language')
            if language_code:
                language = language_mapping.get(language_code, language_code)
                return language

    return None
