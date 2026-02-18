from app.services.genres_service import traducir_generos

def formatear_libro(data):
    autores = [
        c['author']['name'] 
        for c in data.get('contributions', []) 
        if 'author' in c
    ]

    genre = data.get("cached_tags", {}).get("Genre")
    lista_generos = []
    if genre:
        lista_generos = [item.get("tag") for item in genre]

    json_simplificado = {
        "id_api": data.get("id"),
        "titulo": data.get("title"),
        "autores": autores,
        "portada": data.get("image", {}).get("url") if data.get("image") else None,
        "rating": round_num(data.get("rating")),
        "anio": data.get("release_date"),
        "paginas": data.get("pages"),
        "descripcion": data.get("description"),
        "generos": traducir_generos(lista_generos),
        "type": "LIBRO"
    }
    
    return json_simplificado

def round_num(value, decim=2):
    try:
        return str(round(float(value), decim))
    except (TypeError, ValueError):
        return None