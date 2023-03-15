"""Fixtures can be combined into containers.

Fixtures in a container instance must be available without calling them.
"""
from pytypest import fixture


_setup = []


@fixture
def fixt() -> int:
    _setup.append(0)
    return 13


class Container:
    val = fixt


def test_simple():
    assert _setup == []
    assert Container.val is fixt
    assert _setup == []
    c = Container()
    assert _setup == []
    assert c.val == 13
    assert _setup == [0]
