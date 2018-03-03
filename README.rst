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
    >> len(store)
    1

Or using methods:

.. code:: python

    >> store.set('baz', 'qux')
    >> store.get('baz')
    'qux'

You may even use another types:

.. code:: python

    >> store.create_hash('hash', {'my': 'hash'})
    >> store['hash']
    {'my': 'hash'}
    >> store['hash']['foo'] = 'bar'
    {'my': 'hash', 'foo': 'bar'}
    >> store['hash'].update({'baz': 'qux'})
    >> store['hash']
    {'my': 'hash', 'foo': 'bar', 'baz': 'qux'}
