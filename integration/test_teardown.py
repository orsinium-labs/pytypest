"""The basic test for fixtures with teardown.
"""
from typing import Iterator

from pytypest import fixture


_setup = []
_teardown = []


@fixture
def fixt() -> Iterator[int]:
    _setup.append(0)
    yield 13
    _teardown.append(0)


def test_simple():
    n = fixt()
    assert n == 13
    assert _setup == [0]
    assert _teardown == []


def test_after():
    assert _setup == [0]
    assert _teardown == [0]
