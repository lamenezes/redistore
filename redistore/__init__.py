from redis import StrictRedis

from .types import Hash

__all__ = ['Hash', 'get']


def get(**kwargs):
    return RedisStore(**kwargs)


class RedisStore:
    def __init__(self, **kwargs):
        self.redis_client = StrictRedis(**kwargs)

    def __repr__(self):
        connection_kwargs = self.redis_client.connection_pool.connection_kwargs
        return 'RedisStore(host={host!r}, port={port}, db={db})'.format(**connection_kwargs)

    def __getitem__(self, key):
        redis_type = self.redis_client.type(key).decode('utf-8')
        if redis_type == 'none':
            raise KeyError(key)

        if redis_type == 'string':
            value = self.redis_client.get(key)
            return value.decode()
        elif redis_type == 'hash':
            return Hash(key=key, store=self)

        raise NotImplementedError(f'{redis_type} type not supported')

    def __setitem__(self, key, value):
        if isinstance(value, dict):
            Hash(key=key, store=self, data=value)
        else:
            self.redis_client.set(key, value)

    def __delitem__(self, key):
        exists = self.redis_client.delete(key)
        if exists == 0:
            raise KeyError(key)

    def __contains__(self, key):
        return self.redis_client.exists(key) is True
