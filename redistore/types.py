from collections.abc import MutableMapping


class Hash(MutableMapping):
    def __init__(self, redis_client, hash_name):
        self._client = redis_client
        self._hash_name = hash_name

    def __repr__(self):
        return '{}(hash_name={!r}, host={host!r}, port={port}, db={db})'.format(
            type(self).__name__, self._hash_name, **self._client.connection_pool.connection_kwargs
        )

    def __getitem__(self, key):
        value = self._client.hget(self._hash_name, key)
        if value is None:
            raise KeyError(key)
        return value

    def __setitem__(self, key, value):
        self._client.hset(self._hash_name, key, value)

    def __delitem__(self, key):
        exists = self._client.hdel(self._hash_name, key)
        if exists == 0:
            raise KeyError(key)

    def __iter__(self):
        return self._client.hscan_iter(self._hash_name)

    def __len__(self):
        return self._client.hlen(self._hash_name)

    def __contains__(self, key):
        return self._client.hexists(self._hash_name, key)

