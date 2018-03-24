from collections.abc import MutableMapping


class RedisType:
    def __init__(self, key=None, store=None, **kwargs):
        self._key = key
        self._store = store

    def __repr__(self):
        return '{}(key={!r})'.format(type(self).__name__, self._key)


class Hash(RedisType, MutableMapping):
    def __init__(self, key, store, data=None):
        super().__init__(key, store)

        self.hash_name = self._key
        if data:
            self.update(data)

    def __repr__(self):
        r = super().__repr__()[:-1]
        return '{}, data={!r})'.format(r, dict(self))

    def __getitem__(self, key):
        value = self._store.redis_client.hget(self.hash_name, key)
        if value is None:
            raise KeyError(key)
        return value.decode()

    def __setitem__(self, key, value):
        self._store.redis_client.hset(self.hash_name, key, value)

    def __delitem__(self, key):
        exists = self._store.redis_client.hdel(self.hash_name, key)
        if exists == 0:
            raise KeyError(key)

    def __iter__(self):
        return (key.decode() for key in self._store.redis_client.hkeys(self.hash_name))

    def __len__(self):
        return self._store.redis_client.hlen(self.hash_name)

    def __contains__(self, key):
        return self._store.redis_client.hexists(self.hash_name, key)

    def clear_keys(self, keys):
        keys = set(keys)
        inexistent_keys = keys - set(self.keys())
        if inexistent_keys:
            raise KeyError(inexistent_keys)

        for key in keys:
            del self[key]
