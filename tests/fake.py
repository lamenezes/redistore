from unittest import mock

from redistore import RedisStore


class FakeRedisClient(RedisStore):
    def __init__(self):
        self._hash = {}
        kwargs = {'host': 'host', 'port': '6969', 'db': 0}
        self.connection_pool = mock.Mock(connection_kwargs=kwargs)

    def hget(self, hash_name, key):
        try:
            return self._hash[key].encode('utf-8')
        except KeyError:
            return None

    def hset(self, hash_name, key, value):
        self._hash[key] = value

    def hdel(self, hash_name, key):
        try:
            del self._hash[key]
            return 1
        except KeyError:
            return 0

    def hscan_iter(self, hash_name):
        for k, v in self._hash.items():
            yield k.encode('utf-8'), v.encode('utf-8')

    def hlen(self, hash_name):
        return len(self._hash)
