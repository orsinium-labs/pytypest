from pytypest import fixture
from typing import Iterator


_before = False
_after = False


@fixture
def fixt() -> Iterator[int]:
    global _before
    global _after
    _before = True
    yield 13
    _after = True


def test_simple():
    n = fixt()
    assert n == 13
    assert _before
    assert not _after


def test_after():
    assert _before
    assert _after
