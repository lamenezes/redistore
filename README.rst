=========
redistore
=========

.. image:: https://badge.fury.io/py/redistore.svg
    :target: https://badge.fury.io/py/redistore

.. image:: https://travis-ci.org/lamenezes/redistore.svg?branch=master
    :target: https://travis-ci.org/lamenezes/redistore

.. image:: https://coveralls.io/repos/github/lamenezes/redistore/badge.svg?branch=master
    :target: https://coveralls.io/github/lamenezes/redistore?branch=master


Simple python interface for redis 

Installation
============

.. code:: bash

    pip install redistore


Usage
=====

.. code:: python

    >> import redistore
    >> store = redistore.get(host='localhost', port=6379, db=0)

Now you can access and store keys and values with a dict-like interface:

.. code:: python

    >> store['foo'] = 'bar'
    >> store['foo']
    'bar'
    >> 'foo' in store
    True
    >> del store['foo']
    >> store['foo']
    ...
    KeyError: 'foo'

Or using methods:

.. code:: python

    >> store.set('baz', 'qux')
    >> store.get('baz')
    'qux'

``redistore`` support other data types, e.g., hashes. they are used exactly like a dict:

.. code:: python

    >> store['hash'] = {}  # creates a hash without any values
    >> 'my' in store['hash']
    True
    >> store['hash']['my']
    'hash'
    >> store['hash'].update({'baz': 'qux'})
    >> store['hash']['baz']
    'qux'
    >> len(store['hash'])
    2
    >> list(store.keys())
    ['foo', 'bar']
    >> for key, value in store.items():
    ...    print(key, value)
    ...
    my hash
    baz qux
    >> store['other_hash'] = {'foo': 'bar'}  # creates a hash with values
    >> store['other_hash']['foo']
    'bar'
