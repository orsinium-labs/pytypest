from pytypest import fixture
from typing import Iterator


_setup = []
_teardown = []


@fixture
def fixt(a, b) -> Iterator[int]:
    _setup.append(0)
    yield a + b
    _teardown.append(0)


def test_simple1():
    n = fixt(6, b=7)
    assert n == 13
    assert _setup == [0]
    assert _teardown == []


def test_simple2():
    n = fixt(a=3, b=4)
    assert n == 7
    assert _setup == [0, 0]
    assert _teardown == [0]


def test_after():
    assert _setup == [0, 0]
    assert _teardown == [0, 0]
