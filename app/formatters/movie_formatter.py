from app.services.genres_service import traducir_ids
from app.utils.utils import round_num

def formatear_media_tmdb(item, tipo):
    portada = item.get("poster_path")
    return {
        "id_api": item.get("id"),
        "titulo": item.get("title") if item.get("title") else item.get("name"),
        "portada": f"https://image.tmdb.org/t/p/w500/{portada}",
        "descripcion": item.get("overview", ""),
        "puntuacion": round_num(item.get("vote_average")),
        "generos": traducir_ids(item.get("genre_ids")),
        "anio": item.get("release_date") if item.get("release_date") else item.get("first_air_date"),
        "type": tipo
    }
