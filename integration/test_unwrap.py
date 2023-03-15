"""
Teardown for fixtures must be executed in the reverse order to how they are called.

So, the first called fixture is teared down the last.
"""
from __future__ import annotations

from typing import Iterator

from pytypest import fixture


_setup = []
_teardown = []


@fixture
def a() -> Iterator[None]:
    _setup.append('a')
    yield
    _teardown.append('a')


@fixture
def b() -> Iterator[None]:
    _setup.append('b')
    yield
    _teardown.append('b')


@fixture
def c() -> Iterator[None]:
    a()
    _setup.append('c')
    yield
    _teardown.append('c')


def test_simple() -> None:
    c()
    b()
    a()
    assert _setup == ['a', 'c', 'b']


def test_after() -> None:
    assert _teardown == ['b', 'c', 'a']
