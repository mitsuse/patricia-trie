from __future__ import annotations

from typing import Callable
from typing import Dict
from typing import Mapping
from typing import Tuple
from typing import TypeVar

import pytest

import patricia

Benchmark = Callable[[Callable[[], None]], None]


def words100k() -> Tuple[str, ...]:
    import gzip
    import os

    zip_name = os.path.join(
        os.path.abspath(os.path.dirname(__file__)), "words100k.txt.gz"
    )

    return tuple(map(str.rstrip, gzip.open(zip_name, "rt")))


def truncated(words: Tuple[str, ...], length: int, count: int) -> Tuple[str, ...]:
    words = [w for w in words if len(w) >= length]
    prefixes = [w[:length] for w in words[:: int(len(words) / count)]]
    return tuple(prefixes[:count])


def random_words(num: int) -> Tuple[str, ...]:
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


def create_dict(words: Tuple[str, ...]) -> Dict[str, int]:
    return dict((w, i) for i, w in enumerate(words))


def create_trie(words: Tuple[str, ...]) -> patricia.Trie:
    values = {w: i for i, w in enumerate(words)}
    return patricia.Trie(**values)


def get(d: Mapping[str, int], words: Tuple[str, ...]) -> None:
    for w in words:
        try:
            d[w]
        except KeyError:
            ...


def contains(d: Mapping[str, int], words: Tuple[str, ...]) -> None:
    for w in words:
        w in d


def iterate(t: patricia.Trie, prefixes: Tuple[str, ...]) -> None:
    for p in prefixes:
        for _ in t.iter(p):
            ...


@pytest.mark.benchmark(group="build")
def test__dict_build(benchmark: Benchmark) -> None:
    def create() -> None:
        create_dict(WORDS)

    benchmark(create)


@pytest.mark.benchmark(group="get")
def test__dict_get_hits(benchmark: Benchmark) -> None:
    d = create_dict(WORDS)
    benchmark(lambda: get(d, WORDS))


@pytest.mark.benchmark(group="get")
def test__dict_get_misses(benchmark: Benchmark) -> None:
    d = create_dict(WORDS)
    benchmark(lambda: get(d, NON_WORDS))


@pytest.mark.benchmark(group="contains")
def test__dict_contains_hits(benchmark: Benchmark) -> None:
    d = create_dict(WORDS)
    benchmark(lambda: contains(d, WORDS))


@pytest.mark.benchmark(group="contains")
def test__dict_contains_misses(benchmark: Benchmark) -> None:
    d = create_dict(WORDS)
    benchmark(lambda: contains(d, NON_WORDS))


@pytest.mark.benchmark(group="build")
def test__trie_build(benchmark: Benchmark) -> None:
    def create() -> None:
        create_trie(WORDS)

    benchmark(create)


@pytest.mark.benchmark(group="get")
def test__trie_get_hits(benchmark: Benchmark) -> None:
    t = create_trie(WORDS)
    benchmark(lambda: get(t, WORDS))


@pytest.mark.benchmark(group="get")
def test__trie_get_misses(benchmark: Benchmark) -> None:
    t = create_trie(WORDS)
    benchmark(lambda: get(t, NON_WORDS))


@pytest.mark.benchmark(group="contains")
def test__trie_contains_hits(benchmark: Benchmark) -> None:
    t = create_trie(WORDS)
    benchmark(lambda: contains(t, WORDS))


@pytest.mark.benchmark(group="contains")
def test__trie_contains_misses(benchmark: Benchmark) -> None:
    t = create_trie(WORDS)
    benchmark(lambda: contains(t, NON_WORDS))


@pytest.mark.benchmark(group="iter")
def test__trie_iter_3k(benchmark: Benchmark) -> None:
    t = create_trie(WORDS)
    benchmark(lambda: iterate(t, PREFIXES_3k))


@pytest.mark.benchmark(group="iter")
def test__trie_iter_5k(benchmark: Benchmark) -> None:
    t = create_trie(WORDS)
    benchmark(lambda: iterate(t, PREFIXES_5k))


@pytest.mark.benchmark(group="iter")
def test__trie_iter_8k(benchmark: Benchmark) -> None:
    t = create_trie(WORDS)
    benchmark(lambda: iterate(t, PREFIXES_8k))
