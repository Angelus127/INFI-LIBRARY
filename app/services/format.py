from .translate import traducir_generos, traducir_estado, traducir_temporada

def formatear_libro(data):
    book_info = data.get('book', {})

    autores = [
        c['author']['name'] 
        for c in book_info.get('contributions', []) 
        if 'author' in c
    ]

    genre = book_info.get("cached_tags", {}).get("Genre")
    lista_generos = []
    if genre:
        lista_generos = [item.get("tag") for item in genre]

    json_simplificado = {
        "isbn_13": data.get("isbn_13"),
        "isbn_10": data.get("isbn_10"),
        "titulo": data.get("title"),
        "portada": data.get("image", {}).get("url") if data.get("image") else None,
        "editorial": data.get("publisher", {}).get("name") if data.get("publisher") else None,
        "rating": book_info.get("rating"),
        "anio": book_info.get("release_date"),
        "id_api": book_info.get("id"),
        "subtitulo": book_info.get("subtitle"),
        "autores": autores,
        "paginas": book_info.get("pages"),
        "descripcion": book_info.get("description"),
        "generos": traducir_generos(lista_generos)
    }
    
    return json_simplificado

def formatear_media_anilist(item):
    """Limpia y estructura los datos de AniList."""
    kind = None
    titleAll = item.get("title", {})
    origin = item.get("countryOfOrigin")
    format_ = item.get("format")
    if origin == "JP":
        title = titleAll.get("romaji") or titleAll.get("english")
    elif origin == "KR":
        title = titleAll.get("english") or titleAll.get("romaji")  
    elif origin == "CN":
        title = titleAll.get("english") or titleAll.get("romaji")
    
    if format_ == "MANGA":
        if origin == "JP":
            kind = "MANGA"
        elif origin == "KR":
            kind = "MANHWA"
        elif origin == "CN":
            kind = "MANHUA"
    elif format_ in ("TV", "MOVIE", "OVA", "ONA"):
        if origin == "JP":
            kind = "ANIME"
        elif origin == "CN":
            kind = "DONGUA"
    else:
        kind = format_ or "UNKNOWN"
    return {
        "id_api": item.get("id"),
        "titulo": title,
        "portada": item.get("coverImage", {}).get("large"),
        "descripcion": item.get("description", ""),
        "puntuacion_media": item.get("averageScore"),
        "episodios": item.get("episodes"),
        "volumenes": item.get("volumes"),
        "capitulos": item.get("chapters"),
        "generos": traducir_generos(item.get("genres", [])),
        "estado": traducir_estado(item.get("status")),
        "formato": format_,
        "tipo": kind,
        "temporada": traducir_temporada(item.get("season")),
        "anio": item.get("seasonYear"),
        "duracion": item.get("duration"),
        "fuente": "AniList"
    }

def format_json(info):
    library = []
    for fila in info:
        library.append({
            "id": fila[0],
            "categoria": fila[1],
            **fila[2],
            "fecha_agregado": fila[3]
        })
    return library