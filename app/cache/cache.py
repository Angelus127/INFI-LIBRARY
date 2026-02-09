import os
from .memory import MemoryCache
from .redis_cache import RedisCache

DEFAULT_TTL = 60 * 30

def get_cache():
    redis_url = os.getenv("REDIS_URL")

    if redis_url:
        return RedisCache(redis_url)
    
    return MemoryCache()

cache = get_cache()