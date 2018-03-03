from redis import StrictRedis

from .types import Hash


def get(**kwargs):
    return RedisStore(**kwargs)


class RedisStore:
    def __init__(self, **kwargs):
        self.redis_client = StrictRedis(**kwargs)

    def __getitem__(self, key):
        redis_type = self.redis_client.type(key).decode('utf-8')
        if redis_type == 'none':
            raise KeyError(key)

        if redis_type == 'string':
            value = self.redis_client.get(key)
            return str(value)
        elif redis_type == 'hash':
            return Hash(key)
        else:
            raise NotImplementedError(f'{redis_type} type not supported')

    def __setitem__(self, key, value):
        self.redis_client.set(key, value)

    def __delitem__(self, key):
        pass
