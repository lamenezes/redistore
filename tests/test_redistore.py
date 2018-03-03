from unittest import mock

import redistore


@mock.patch('redistore.RedisStore')
def test_get(mock_store):
    kwargs = {'host': 'http://host/', 'port': 666, 'db': 69}

    assert redistore.get(**kwargs)

    mock_store.assert_called_with(**kwargs)
