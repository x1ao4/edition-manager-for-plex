import requests
from configparser import ConfigParser

def get_Language(server, token, movie_id, excluded_languages):
    config = ConfigParser()
    config.read('config/config.ini')
    skip_multiple_audio_tracks = config.getboolean('language', 'skip_multiple_audio_tracks', fallback=False)

    headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
    response = requests.get(f'{server}/library/metadata/{movie_id}', headers=headers)
    data = response.json()

    language_mapping = {
        'Afrikaans': 'Afrikaans',
        'Akan': 'Akan',
        'Shqip': 'Albanian',
        'አማርኛ': 'Amharic',
        'العربية': 'Arabic',
        'Aragonés': 'Aragonese',
        'հայերեն': 'Armenian',
        'অসমীয়া': 'Assamese',
        'Asturianu': 'Asturian',
        'Azərbaycan': 'Azerbaijani',
        'Башҡортса': 'Bashkir',
        'Euskara': 'Basque',
        'Беларуская': 'Belarusian',
        'বাংলা': 'Bengali',
        'Bosanski': 'Bosnian',
        'Brezhoneg': 'Breton',
        'Български': 'Bulgarian',
        'ဗမာစာ': 'Burmese',
        'Català': 'Catalan',
        'Cebuano': 'Cebuano',
        'ᏣᎳᎩ': 'Cherokee',
        '中文': 'Chinese',
        '广东话': 'Cantonese',
        '普通话': 'Mandarin',
        'Corsu': 'Corsican',
        'Hrvatski': 'Croatian',
        'Čeština': 'Czech',
        'Dansk': 'Danish',
        'ދިވެހި': 'Dhivehi',
        'Nederlands': 'Dutch',
        'ཇོང་ཁ': 'Dzongkha',
        'English': 'English',
        'Esperanto': 'Esperanto',
        'Eesti': 'Estonian',
        'Føroyskt': 'Faroese',
        'Fiji Hindi': 'Fiji Hindi',
        'Filipino': 'Filipino',
        'Suomi': 'Finnish',
        'Français': 'French',
        'Frysk': 'Frisian',
        'Fulfulde': 'Fulah',
        'Galego': 'Galician',
        'ქართული': 'Georgian',
        'Deutsch': 'German',
        'Ελληνικά': 'Greek',
        'Kalaallisut': 'Greenlandic',
        'ગુજરાતી': 'Gujarati',
        'Kreyòl ayisyen': 'Haitian Creole',
        'Hausa': 'Hausa',
        'ʻŌlelo Hawaiʻi': 'Hawaiian',
        'עברית': 'Hebrew',
        'हिन्दी': 'Hindi',
        'Hmong': 'Hmong',
        'Hungarian': 'Hungarian',
        'Magyar': 'Hungarian',
        'Íslenska': 'Icelandic',
        'Igbo': 'Igbo',
        'Ilokano': 'Ilokano',
        'Bahasa Indonesia': 'Indonesian',
        'Gaeilge': 'Irish',
        'Italiano': 'Italian',
        '日本語': 'Japanese',
        'Basa Jawa': 'Javanese',
        'ಕನ್ನಡ': 'Kannada',
        'Қазақ тілі': 'Kazakh',
        'ភាសាខ្មែរ': 'Khmer',
        'Kinyarwanda': 'Kinyarwanda',
        'Kiswahili': 'Swahili',
        '한국어': 'Korean',
        'Kurdî': 'Kurdish',
        'Кыргызча': 'Kyrgyz',
        'ລາວ': 'Lao',
        'Latviešu': 'Latvian',
        'Lietuvių': 'Lithuanian',
        'Lëtzebuergesch': 'Luxembourgish',
        'Македонски': 'Macedonian',
        'Malagasy': 'Malagasy',
        'Bahasa Melayu': 'Malay',
        'മലയാളം': 'Malayalam',
        'Malti': 'Maltese',
        'Māori': 'Maori',
        'मराठी': 'Marathi',
        'Монгол': 'Mongolian',
        'myn': 'Mayan',
        "Mayaq'ik": 'Mayan',
        'magyar': 'Hungarian',
        'नेपाली': 'Nepali',
        'Norsk': 'Norwegian',
        'Occitan': 'Occitan',
        'ଓଡ଼ିଆ': 'Odia',
        'Afaan Oromoo': 'Oromo',
        'پښتو': 'Pashto',
        'فارسی': 'Persian',
        'Polski': 'Polish',
        'Português': 'Portuguese',
        'ਪੰਜਾਬੀ': 'Punjabi',
        'Quechua': 'Quechua',
        'Română': 'Romanian',
        'Rumantsch': 'Romansh',
        'Русский': 'Russian',
        'Samoan': 'Samoan',
        'Sängö': 'Sango',
        'Gaelic': 'Scottish Gaelic',
        'Српски': 'Serbian',
        'Sesotho': 'Sesotho',
        'Setswana': 'Setswana',
        'Shona': 'Shona',
        'සිංහල': 'Sinhala',
        'Slovenčina': 'Slovak',
        'Slovenščina': 'Slovenian',
        'Soomaaliga': 'Somali',
        'Español': 'Spanish',
        'Basa Sunda': 'Sundanese',
        'Svenska': 'Swedish',
        'Tagalog': 'Tagalog',
        'தமிழ்': 'Tamil',
        'Татарча': 'Tatar',
        'తెలుగు': 'Telugu',
        'ไทย': 'Thai',
        'བོད་ཡིག': 'Tibetan',
        'Tigrinya': 'Tigrinya',
        'Türkçe': 'Turkish',
        'Türkmen': 'Turkmen',
        'Українська': 'Ukrainian',
        'اردو': 'Urdu',
        'Uyghur': 'Uyghur',
        'Tiếng Việt': 'Vietnamese',
        'Cymraeg': 'Welsh',
        'Wolof': 'Wolof',
        'isiXhosa': 'Xhosa',
        'ייִדיש': 'Yiddish',
        'Yorùbá': 'Yoruba',
        'isiZulu': 'Zulu'
    }

    if 'MediaContainer' in data and 'Metadata' in data['MediaContainer']:
        metadata = data['MediaContainer']['Metadata'][0]
        if 'Media' in metadata:
            audio_tracks = []
            for media in metadata['Media']:
                if 'Part' in media:
                    for part in media['Part']:
                        if 'Stream' in part:
                            for stream in part['Stream']:
                                if stream['streamType'] == 2:  # 2 is for audio streams
                                    language = stream.get('language')
                                    if language:
                                        audio_tracks.append(language)

            # If there are multiple audio tracks and skip_multiple_audio_tracks is True, return None
            if len(audio_tracks) > 1 and skip_multiple_audio_tracks:
                return None

            # Process single audio track or when skip_multiple_audio_tracks is False
            for language in audio_tracks:
                language = language_mapping.get(language, language)
                if language not in ['Unknown', 'Undetermined', 'Undetermined language'] and language not in excluded_languages:
                    return language

    return None
