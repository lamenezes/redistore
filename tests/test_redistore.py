from unittest import mock

import pytest

from redistore import Hash, get


@mock.patch('redistore.RedisStore')
def test_get(mock_store):
    kwargs = {'host': 'http://host/', 'port': 666, 'db': 69}

    assert get(**kwargs)

    mock_store.assert_called_with(**kwargs)


def test_redis_store(store):
    assert store.redis_client
    assert store.connection_kwargs


def test_redis_store_setitem_string(store):
    store['foo'] = 'foo'
    assert 'foo' in store


def test_redis_store_setitem_hash(store):
    store['hash'] = {'foo': 'foohash', 'bar': 'barhash'}

    assert 'hash' in store
    assert isinstance(store['hash'], Hash)


def test_redis_store_getitem_string(store):
    store['foo'] = 'foo'
    assert store['foo'] == 'foo'


def test_redis_store_getitem_hash(store):
    store['hash'] = {'foo': 'foohash', 'bar': 'barhash'}

    store_hash = store['hash']
    assert isinstance(store_hash, Hash)
    assert store['hash']['foo'] == 'foohash'
    assert store['hash']['bar'] == 'barhash'


def test_redis_store_getitem_other(store):
    store.redis_client.lpush('list', 1)

    with pytest.raises(NotImplementedError):
        store['list']


def test_redis_store_getitem_inexistent_key(store):
    with pytest.raises(KeyError):
        store['foo']


def test_redis_store_delitem(store):
    store['foo'] = 'foo'
    store['bar'] = 'bar'

    del store['foo']

    assert 'foo' not in store
    assert 'bar' in store


def test_redis_store_delitem_invalid_key(store):
    with pytest.raises(KeyError):
        del store['foo']
