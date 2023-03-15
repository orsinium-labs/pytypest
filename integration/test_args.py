"""Fixtures with arguments aren't cached.
"""
from typing import Iterator

from pytypest import fixture


_setup = []


@fixture
def fixt(a, b) -> Iterator[int]:
    _setup.append(a)
    return a + b


def test_simple1():
    n = fixt(6, b=7)
    assert n == 13
    assert _setup == [6]


def test_simple2():
    n = fixt(a=3, b=4)
    assert n == 7
    assert _setup == [6, 3]


def test_double():
    n1 = fixt(a=3, b=4)
    assert n1 == 7
    assert _setup == [6, 3, 3]
    n1 = fixt(a=4, b=5)
    assert n1 == 9
    assert _setup == [6, 3, 3, 4]


def test_after():
    assert _setup == [6, 3, 3, 4]
