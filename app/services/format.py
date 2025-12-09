from .translate import traducir_generos, traducir_estado, traducir_temporada

def formatear_libro(item):
    """Limpia y estructura los datos de Google Books."""
    info = item.get("volumeInfo", {})
    imagen = info.get("imageLinks", {}).get("thumbnail", "")
    isbn = ""
    for i in info.get("industryIdentifiers", []):
        if i.get("type") == "ISBN_13":
            isbn = i.get("identifier")
            break

    return {
        "id_api": item.get("id"),
        "titulo": info.get("title"),
        "autores": info.get("authors", []),
        "isbn": isbn,
        "generos": traducir_generos(info.get("categories", [])),
        "paginas": info.get("pageCount"),
        "portada": imagen,
        "resumen": info.get("description", ""),
        "anio": info.get("publishedDate", ""),
        "fuente": "GoogleBooks"
    }

def formatear_media_anilist(item):
    """Limpia y estructura los datos de AniList."""
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