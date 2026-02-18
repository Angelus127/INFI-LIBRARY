from app.services.genres_service import traducir_generos

def formatear_juego(data):
    plataformas = [p['platform']['name'] for p in data.get("platforms", [])]
    genres = [g['name'] for g in data.get("genres", [])]
    json_simplificado = {
        "id_api": data.get('id'),
        "titulo": data.get('name'),
        "portada": data.get('background_image'),
        "puntuacion": data.get('metacritic'),
        "generos": traducir_generos(genres),
        "anio": data.get('released'),
        "plataforma": plataformas,
        "type": "VIDEOJUEGO"
    }
    return json_simplificado