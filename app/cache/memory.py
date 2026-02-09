import time
from .base import BaseCache

class MemoryCache(BaseCache):
    def __init__(self):
        self._store = {}
        self._expiry = {}

    def _is_expired(self, key):
        exp = self._expiry.get(key)
        return exp is not None and time.time() > exp

    def get(self, key):
        if key not in self._store:
            return None

        if self._is_expired(key):
            self.delete(key)
            return None

        return self._store[key]

    def set(self, key, value, ttl=None):
        self._store[key] = value
        if ttl:
            self._expiry[key] = time.time() + ttl
        else:
            self._expiry.pop(key, None)
    
    def delete(self, key):
        self._store.pop(key, None)
        self._expiry.pop(key, None)
