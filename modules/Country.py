import requests

def get_Country(server, token, movie_id):
    # Send request to get metadata
    headers = {'X-Plex-Token': token, 'Accept': 'application/json'}
    response = requests.get(f'{server}/library/metadata/{movie_id}', headers=headers)
    data = response.json()

    # Extract country information from the response
    countries = data['MediaContainer']['Metadata'][0].get('Country', [])

    # If no country information is found, return None
    if not countries:
        return None

    # Extract the name of each country
    country_names = [country['tag'] for country in countries]
    
    # Join multiple countries with a delimiter
    country = ' · '.join(country_names)

    return country