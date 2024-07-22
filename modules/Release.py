import re
import requests

def get_Release(file_name, server, token, movie_id):
    # Define release versions with their English names
    releases = {
        r'\b(Special Edition)\b': 'Special Edition',
        r'\b(Restored Edition)\b': 'Restored',
        r'\b(Remastered Edition)\b': 'Remastered',
        r'\b(3D Edition|3D)\b': '3D',
        r'\b(IMAX Edition|IMAX)\b': 'IMAX',
        r'\b(Collector\'s Edition|Collectors Edition)\b': 'Collector\'s Edition',
        r'\b(Anniversary Edition)\b': 'Anniversary Edition',
        r'\b(Ultimate Edition)\b': 'Ultimate Edition',
        r'\b(Limited Edition)\b': 'Limited Edition',
        r'\b(Commemorative Edition)\b': 'Commemorative Edition',
        r'\b(Deluxe Edition)\b': 'Deluxe Edition',
        r'\b(Director\'s Signature Edition|Director\'s Signature)\b': 'Director\'s Signature Edition',
        r'\b(Criterion Collection|CC)\b': 'Criterion Collection'
    }

    # Extract the edition information from the filename
    edition_match = re.search(r'\{edition-(.*?)\}', file_name)
    if edition_match:
        edition_info = edition_match.group(1)
        
        # Check edition info for release version
        matched_releases = []
        for release_pattern, release_name in releases.items():
            if re.search(release_pattern, edition_info, re.IGNORECASE):
                matched_releases.append(release_name)

        # If release versions are found, join them with ' · '
        if matched_releases:
            return ' · '.join(matched_releases)

    # If no release version found in filename, return None
    return None