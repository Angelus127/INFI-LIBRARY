class BaseCache:
    def get(self, key):
        raise NotImplementedError

    def set(self, key, value, ttl:None):
        raise NotImplementedError

    def delete(self, key):
        raise NotImplementedError

    def set_many(self, items, key_field="id_api", ttl=None):
        for item in items:
            if not isinstance(item, dict):
                raise TypeError(
                    f"Cache esperaba dict, recibió {type(item)}"
                )
            self.set(str(item[key_field]), item, ttl)