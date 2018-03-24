from unittest import mock

import pytest

from fakeredis import FakeStrictRedis


class MyFakeStrictRedis(FakeStrictRedis):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        connection_kwargs = {'host': 'host', 'port': '6969', 'db': 0}
        self.connection_pool = mock.Mock(connection_kwargs=connection_kwargs)


@pytest.fixture
def store(request):
    from redistore import RedisStore

    fake_redis_client = MyFakeStrictRedis()
    store = RedisStore()
    store.redis_client = fake_redis_client

    request.addfinalizer(fake_redis_client.flushall)
    return store
