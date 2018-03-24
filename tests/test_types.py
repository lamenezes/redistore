import pytest

from redistore.types import Hash


@pytest.fixture
def redis_hash(store):
    redis_hash = Hash('hashish', store)
    redis_hash.clear()
    return redis_hash


def test_redis_hash(redis_hash):
    assert redis_hash._store
    assert redis_hash.hash_name
    assert 'key' in repr(redis_hash)
    assert "host='" in repr(redis_hash)


def test_redis_hash_contains(redis_hash):
    assert 'foo' not in redis_hash

    redis_hash['foo'] = redis_hash
    assert 'foo' in redis_hash
    assert 'bar' not in redis_hash


def test_redis_hash_get_set_del_len(redis_hash):
    assert len(redis_hash) == 0
    redis_hash['foo'] = 'fooz'
    assert redis_hash['foo'] == 'fooz'
    assert len(redis_hash) == 1

    redis_hash['bar'] = 'barz'
    assert redis_hash['bar'] == 'barz'
    assert len(redis_hash) == 2

    assert set(redis_hash) == {'foo', 'bar'}

    del redis_hash['bar']
    assert len(redis_hash) == 1
    del redis_hash['foo']
    assert len(redis_hash) == 0


def test_redis_hash_create_and_store(store):
    data = {
        'foo': 'fooz',
        'bar': 'barz',
        'baz': 'bazz',
    }
    redis_hash = Hash('dcg', store, data=data)

    assert dict(redis_hash) == data


def test_redis_hash_getitem_keyerror(redis_hash):
    with pytest.raises(KeyError):
        redis_hash['nx']


def test_redis_hash_delitem_keyerror(redis_hash):
    with pytest.raises(KeyError):
        del redis_hash['nx']


def test_redis_hash_clear_keys(redis_hash):
    redis_hash['foo'] = 'foo'
    redis_hash['bar'] = 'bar'
    redis_hash['baz'] = 'baz'

    redis_hash.clear_keys(('bar', 'baz'))

    assert len(redis_hash) == 1
    assert 'foo' in redis_hash


def test_redis_hash_clear_keys_inexistent_keys(redis_hash):
    redis_hash['foo'] = 'foo'

    with pytest.raises(KeyError):
        redis_hash.clear_keys(('bar', 'baz'))

    with pytest.raises(KeyError):
        redis_hash.clear_keys(('foo', 'baz'))
