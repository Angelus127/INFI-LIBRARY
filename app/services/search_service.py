from app.apis.animes_api import search_anilist
from app.apis.books_api import search_books
from app.formatters.anime_formatter import formatear_media_anilist
from app.formatters.book_formatter import formatear_libro
from app.cache.cache import cache, DEFAULT_TTL

def search(title, media_type):
    if media_type == "LIBRO":
        raw_items = search_books(title)
        results = [formatear_libro(b) for b in raw_items]
    else:
        raw_items = search_anilist(title, media_type)
        results = [formatear_media_anilist(m) for m in raw_items]
    
    cache.set_many(results, ttl=DEFAULT_TTL)
    return results