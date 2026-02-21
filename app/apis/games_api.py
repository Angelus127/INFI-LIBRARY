import requests, os

class GamesApiError(Exception):
    pass

import os
import requests

def search_games(title):
    base_url = "https://api.rawg.io/api/games"
    api_key = os.getenv('GAMES_API')
    
    params = {
        'key': api_key,
        'search': title,
        'page_size': 20
    }

    try:
        response = requests.get(base_url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get('results', [])
        
    except Exception as e:
        raise GamesApiError("Error al conectar con la búsqueda de RAWG") from e