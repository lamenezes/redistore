from unittest import mock

import pytest

from redistore.types import Hash
from .fake import FakeRedisClient


@pytest.fixture
def store():
    return mock.Mock(client=FakeRedisClient())


@pytest.fixture
def redis_hash(store):
    return Hash(store, 'hashish')


@pytest.fixture
def mock_redis_hash(store):
    return Hash(mock.MagicMock(), 'hashish')


def test_redis_hash(redis_hash):
    assert redis_hash._store
    assert redis_hash._hash_name
    assert 'hash_name' in repr(redis_hash)
    assert "host='" in repr(redis_hash)

    assert len(redis_hash) == 0
    redis_hash['foo'] = 'fooz'
    assert redis_hash['foo'] == b'fooz'
    assert len(redis_hash) == 1

    redis_hash['bar'] = 'barz'
    assert redis_hash['bar'] == b'barz'
    assert len(redis_hash) == 2

    assert set(redis_hash) == set([(b'foo', b'fooz'), (b'bar', b'barz')])

    del redis_hash['bar']
    assert len(redis_hash) == 1
    del redis_hash['foo']
    assert len(redis_hash) == 0


def test_redis_hash_getitem_keyerror(redis_hash):
    with pytest.raises(KeyError):
        redis_hash['nx']


def test_redis_hash_delitem_keyerror(redis_hash):
    with pytest.raises(KeyError):
        del redis_hash['nx']


def test_redis_hash_contains(mock_redis_hash):
    key = 'eita'
    assert key in mock_redis_hash

    mock_redis_hash._store.client.hexists.assert_called_with(mock_redis_hash._hash_name, key)


def test_redis_hash_len(mock_redis_hash):
    assert len(mock_redis_hash)

    mock_redis_hash._store.client.hlen.assert_called_with(mock_redis_hash._hash_name)
