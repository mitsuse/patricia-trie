from __future__ import annotations

import pytest


def words100k():
    import gzip
    import os

    zip_name = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "words100k.txt.gz"
    )

    return tuple(map(str.rstrip, gzip.open(zip_name, "rt")))


def truncated(words, length, count):
    words = [w for w in words if len(w) >= length]
    prefixes = [w[:length] for w in words[:: int(len(words) / count)]]
    return prefixes[:count]


def random_words(num):
    import random
    import string

    russian = "абвгдеёжзиклмнопрстуфхцчъыьэюя"
    alphabet = russian + string.ascii_letters

    return tuple(
        [
            "".join(random.choice(alphabet) for x in range(random.randint(1, 15)))
            for y in range(num)
        ]
    )


WORDS = words100k()
NON_WORDS = random_words(100000)
PREFIXES_3k = truncated(WORDS, 3, 1000)
PREFIXES_5k = truncated(WORDS, 5, 1000)
PREFIXES_8k = truncated(WORDS, 8, 1000)


def create_dict(words):
    return dict((word, len(word)) for word in words)


def create_trie(words):
    from patricia import trie

    values = {k: i for i, k in enumerate(words)}
    return trie(**values)


def get(d, words):
    for w in words:
        try:
            d[w]
        except KeyError:
            ...


def contains(d, words):
    for w in words:
        w in d


def iterate(t, prefixes):
    for p in prefixes:
        for _ in t.iter(p):
            ...


@pytest.mark.benchmark(group="build")
def test__dict_build(benchmark):
    benchmark(lambda: create_dict(WORDS))


@pytest.mark.benchmark(group="get")
def test__dict_get_hits(benchmark):
    d = create_dict(WORDS)
    benchmark(lambda: get(d, WORDS))


@pytest.mark.benchmark(group="get")
def test__dict_get_misses(benchmark):
    d = create_dict(WORDS)
    benchmark(lambda: get(d, NON_WORDS))


@pytest.mark.benchmark(group="contains")
def test__dict_contains_hits(benchmark):
    d = create_dict(WORDS)
    benchmark(lambda: contains(d, WORDS))


@pytest.mark.benchmark(group="contains")
def test__dict_contains_misses(benchmark):
    d = create_dict(WORDS)
    benchmark(lambda: contains(d, NON_WORDS))


@pytest.mark.benchmark(group="items")
def test__dict_items(benchmark):
    d = create_dict(WORDS)
    benchmark(lambda: d.items())


@pytest.mark.benchmark(group="items")
def test__dict_keys(benchmark):
    d = create_dict(WORDS)
    benchmark(lambda: d.keys())


@pytest.mark.benchmark(group="items")
def test__dict_values(benchmark):
    d = create_dict(WORDS)
    benchmark(lambda: d.values())


@pytest.mark.benchmark(group="build")
def test__trie_build(benchmark):
    benchmark(lambda: create_trie(WORDS))


@pytest.mark.benchmark(group="get")
def test__trie_get_hits(benchmark):
    t = create_trie(WORDS)
    benchmark(lambda: get(t, WORDS))


@pytest.mark.benchmark(group="get")
def test__trie_get_misses(benchmark):
    t = create_trie(WORDS)
    benchmark(lambda: get(t, NON_WORDS))


@pytest.mark.benchmark(group="contains")
def test__trie_contains_hits(benchmark):
    t = create_trie(WORDS)
    benchmark(lambda: contains(t, WORDS))


@pytest.mark.benchmark(group="contains")
def test__trie_contains_misses(benchmark):
    t = create_trie(WORDS)
    benchmark(lambda: contains(t, NON_WORDS))


@pytest.mark.benchmark(group="items")
def test__trie_items(benchmark):
    t = create_trie(WORDS)
    benchmark(lambda: t.items())


@pytest.mark.benchmark(group="items")
def test__trie_keys(benchmark):
    t = create_trie(WORDS)
    benchmark(lambda: t.keys())


@pytest.mark.benchmark(group="items")
def test__trie_values(benchmark):
    t = create_trie(WORDS)
    benchmark(lambda: t.values())


@pytest.mark.benchmark(group="iter")
def test__trie_iter_3k(benchmark):
    t = create_trie(WORDS)
    benchmark(lambda: iterate(t, PREFIXES_3k))


@pytest.mark.benchmark(group="iter")
def test__trie_iter_5k(benchmark):
    t = create_trie(WORDS)
    benchmark(lambda: iterate(t, PREFIXES_5k))


@pytest.mark.benchmark(group="iter")
def test__trie_iter_8k(benchmark):
    t = create_trie(WORDS)
    benchmark(lambda: iterate(t, PREFIXES_8k))
