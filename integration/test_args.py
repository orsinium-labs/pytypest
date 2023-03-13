from pytypest import fixture
from typing import Iterator


_setup = []


@fixture
def fixt(a, b) -> Iterator[int]:
    _setup.append(0)
    return a + b


def test_simple1():
    n = fixt(6, b=7)
    assert n == 13
    assert _setup == [0]


def test_simple2():
    n = fixt(a=3, b=4)
    assert n == 7
    assert _setup == [0, 0]


def test_after():
    assert _setup == [0, 0]
