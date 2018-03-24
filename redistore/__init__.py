from redis import StrictRedis

from .types import Hash

__all__ = ['Hash', 'get']


def get(**kwargs):
    return RedisStore(**kwargs)


class RedisStore:
    def __init__(self, **kwargs):
        self.redis_client = StrictRedis(**kwargs)

    @property
    def connection_kwargs(self):
        return self.redis_client.connection_pool.connection_kwargs

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
        self.redis_client.set(key, value)

    def __delitem__(self, key):
        pass
