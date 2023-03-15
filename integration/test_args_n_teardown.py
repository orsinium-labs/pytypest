"""Teardown must be executed for fixtures with arguments.
"""
from typing import Iterator

from pytypest import fixture


_setup = []
_teardown = []


@fixture
def fixt(a, b) -> Iterator[int]:
    _setup.append(a)
    yield a + b
    _teardown.append(a)


def test_simple1():
    n = fixt(6, b=7)
    assert n == 13
    assert _setup == [6]
    assert _teardown == []


def test_simple2():
    n1 = fixt(a=3, b=4)
    assert n1 == 7
    n2 = fixt(a=5, b=4)
    assert n2 == 9
    assert _setup == [6, 3, 5]
    assert _teardown == [6]


def test_after():
    assert _setup == [6, 3, 5]
    assert _teardown == [6, 3, 5]
