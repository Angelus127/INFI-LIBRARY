from app.services.genres_service import traducir_generos

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
        tipo = "MANGA"
    elif format_ in ("TV", "MOVIE", "OVA", "ONA"):
        if origin == "JP":
            kind = "ANIME"
        elif origin == "CN":
            kind = "DONGUA"
        tipo = "ANIME"
    else:
        kind = format_ or "UNKNOWN"
        tipo = None
    return {
        "id_api": item.get("id"),
        "titulo": title,
        "portada": item.get("coverImage", {}).get("large"),
        "descripcion": item.get("description", ""),
        "puntuacion_media": item.get("averageScore"),
        "generos": traducir_generos(item.get("genres", [])),
        "tipo": kind,
        "anio": item.get("seasonYear"),
        "type": tipo
    }