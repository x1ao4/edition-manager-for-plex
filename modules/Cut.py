import re
import requests

def get_Cut(file_name, server, token, movie_id):
    # Define cut versions and their uniform output
    cuts = {
        r'\b(Theatrical Cut|Theatrical)\b': 'Theatrical Cut',
        r'\b(Director\'s Cut|Directors Cut|DC)\b': 'Directors Cut',
        r'\b(Producer\'s Cut|Producer Cut)\b': 'Producers Cut',
        r'\b(Extended Cut|Extended Edition|Extended)\b': 'Extended',
        r'\b(Unrated Cut|Unrated)\b': 'Unrated',
        r'\b(The Final Cut|Final Cut)\b': 'Final Cut',
        r'\b(Television Cut|Television Version|Television)\b': 'Television Cut',
        r'\b(International Cut)\b': 'International Cut',
        r'\b(Redux|Redux Version|Redux Cut)\b': 'Redux'
    }

    # Extract the edition information from the filename
    edition_match = re.search(r'\{edition-(.*?)\}', file_name)
    if edition_match:
        edition_info = edition_match.group(1)
        
        # Check edition info for cut version
        for cut_pattern, uniform_cut in cuts.items():
            if re.search(cut_pattern, edition_info, re.IGNORECASE):
                return uniform_cut

    # If no cut version found in filename, return None
    return None