patricia-trie
=============

A pure Python 2.7+ implementation of a PATRICIA trie for effcient matching
of string collections on text.

Note that you probably first want to have a look at the Python wrapper
`marisa-trie`_ or its `PyPi package <https://github.com/kmike/marisa-trie/>`_
before using particia-trie; according to simple timeit comparisons, these
wrappers for the C-based MARISA library are about twice as fast as this pure
Python implementation.

`patricia-trie`_ does have its merits, however - it is small, clear, and
has a very clean interface that imitates the `dict` API and works with Py3k.

Installation
------------

::

  pip install patricia-trie

Usage
-----

::

    >>> T = trie('root', key='value', king='kong') # a root value and two pairs
    >>> T['four'] = None # setting new values as in a dict
    >>> '' in T # check if the value exits (note: the [empty] root is '')
    True
    >>> 'kong' in T # existence checks as in a dict
    False
    >>> T['king'] # get the value for an exact key ... as in a dict
    'kong'
    >>> T['kong'] # error from non-existing keys (as in a dict)
    Traceback (most recent call last):
        ...
    KeyError: 'kong'
    >>> len(T) # count keys ("terminals") in the tree
    4
    >>> sorted(T) # plus "traditional stuff": .keys(), .values(), and .items()
    ['', 'four', 'key', 'king']
    >>> # scanning a string S with key(S), value(S), and item(S):
    >>> S = 'keys and kewl stuff'
    >>> T.key(S) # report the (longest) key that is a prefix of S
    'key'
    >>> T.value(S, 9) # using offsets; NB: a root value always matches!
    'root'
    >>> del T[''] # interlude: deleting keys (here, the root)
    >>> T.item(S, 9) # raise error if no key is a prefix of S
    Traceback (most recent call last):
        ...
    KeyError: 'k'
    >>> # info: the error string above contains the matched path so far
    >>> T.item(S, 9, default=None) # avoid the error by specifying a default
    (None, None)
    >>> # iterate all matching content with keys(S), values(S), and items(S):
    >>> list(T.items(S))
    [('key', 'value')]
    >>> T.isPrefix('k') # reverse lookup: check if S is a prefix of any key
    True
    >>> T.isPrefix('kong')
    False
    >>> sorted(T.iter('k')) # and get all keys that have S as prefix
    ['key', 'king']

*Deleting* entries is a "half-supported" operation only. The key appears
"removed", but the trie is not actually changed, only the node state is
changed from terminal to non-terminal. I.e., if you frequently delete keys,
the compaction will become fragmented and less efficient. To mitigate this
effect, make a copy of the trie (using a copy constructor idiom)::

    T = trie(**T)

If you are only interested in scanning for the *presence* of keys, but do not
care about mapping a value to each key, using ``None`` as the value of your
keys and scanning with ``key(S, None, start=i)`` at every offset ``i`` in the
string ``S`` is perfectly fine (because the return value will be the key
string iff a full match was made and ``None`` otherwise)::

    >>> T = trie(present=None)
    >>> T.key('is absent here', None, start=3) # start scanning at offset 3
    >>> T.key('is present here', None, start=3) # start scanning at offset 3
    'present'

API
---

trie(``*value``, ``**branch``)
    | Create a new tree node.
    | Any arguments will be used as the ``value`` of this node.
    | If keyword arguments are given, they initialize a whole ``branch``.
    | Note that `None` is a valid value for a node.

trie.isPrefix(``prefix``)
    | Return True if any key starts with ``prefix``.

trie.item(``string``, ``start=0``, ``end=None``, ``default=NULL``)
    | Return the key, value pair of the longest key that is a prefix of ``string`` (beginning at ``start`` and ending at ``end``).
    | If no key matches, raise a `KeyError` or return the `None`, ``default`` pair if any ``default`` value was set.

trie.items([``string`` [, ``start`` [, ``end`` ]]])
    Return all key, value pairs (for keys that are a prefix of ``string``
    (beginning at ``start`` (and terminating before ``end``))).

trie.iter(``prefix``)
    Return an iterator over all keys that start with ``prefix``.

trie.key(``string``, ``start=0``, ``end=None``, ``default=NULL``)
    | Return the longest key that is a prefix of ``string`` (beginning at ``start`` and ending at ``end``).
    | If no key matches, raise a `KeyError` or return the ``default`` value if it was set.

trie.keys([``string`` [, ``start`` [, ``end`` ]]])
    Return all keys (that are a prefix of ``string``
    (beginning at ``start`` (and terminating before ``end``))).

trie.value(``string``, ``start=0``, ``end=None``, ``default=NULL``)
    | Return the value of the longest key that is a prefix of ``string`` (beginning at ``start`` and ending at ``end``).
    | If no key matches, raise a `KeyError` or return the ``default`` value if it was set.

trie.values([``string`` [, ``start`` [, ``end`` ]]])
    Return all values (for keys that are a prefix of ``string``
    (beginning at ``start`` (and terminating before ``end``))).
   
   
Copyright
---------

Copyright 2013, Florian Leitner. All rights reserved.