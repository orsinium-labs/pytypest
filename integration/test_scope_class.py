"""Teardown for class-scoped fixtures is executed after leaving the class scope.
"""
from typing import Iterator

from pytypest import Scope, fixture


_setup = []
_teardown = []


@fixture(scope=Scope.CLASS)
def fixt() -> Iterator[int]:
    _setup.append(0)
    yield 13
    _teardown.append(0)


class TestClass:
    def test_simple_1(self):
        n = fixt()
        assert n == 13
        assert _setup == [0]
        assert _teardown == []

    def test_simple_2(self):
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
