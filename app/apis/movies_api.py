import requests, os

class MovieApiError(Exception):
    pass

base_url = "https://api.themoviedb.org/3"
api = os.getenv('MOVIES_API')

def search_api(endpoint, params):
    try:
        response = requests.get(f"{base_url}/{endpoint}", params=params)
        return response.json().get("results", [])   
    except Exception as e:
        raise MovieApiError("TMDB no respondio correctamente") from e

def search_tmdb(title, type):
    params = {
        "api_key": api,
        "query": title,
        "language": "es-ES",
    }

    if type == "PELICULA":
        return search_api("search/movie", params)

    elif type == "SERIE":
        return search_api("search/tv", params)

    elif type == "DORAMA":
        data = search_api("search/tv", params)
        return get_doramas(data)
        

def get_doramas(data):
    drama = {'KR', 'JP', 'CN', 'TH'}
    genero = 16
    doramas = [
        serie for serie in data
        if any(p in drama for p in serie.get("origin_country", []))
        and genero not in serie.get("genre_ids", [])
    ]
    return doramas
