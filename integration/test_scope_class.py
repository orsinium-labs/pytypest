from pytypest import fixture, Scope
from typing import Iterator


_setup = []
_teardown = []


@fixture(scope=Scope.CLASS)
def fixt() -> Iterator[int]:
    _setup.append(0)
    yield 13
    _teardown.append(0)


class TestClass:
    def test_simple(self):
        n = fixt()
        assert n == 13
        assert _setup == [0]
        assert _teardown == []

    def test_after_test(self):
        assert _setup == [0]
        assert _teardown == []


def test_after_class():
    assert _setup == [0]
    assert _teardown == [0]
