import json
import redis
from .base import BaseCache

class RedisCache(BaseCache):
    def __init__(self, redis_url):
        self.client = redis.Redis.from_url(
            redis_url,
            decode_reponses=True
        )
    
    def get(self, key):
        data = self.client.get(key)
        return json.loads(data) if data else None
    
    def set(self, key, value, ttl=None):
        data = json.dumps(value)
        if ttl:
            self.client.setex(key, ttl, data)
        else:
            self.client.set(key, data)

    def delete(self, key):
        self.client.delete(key)