"""The most basic test for the most basic fixture.
"""
from pytypest import fixture


@fixture
def fixt() -> int:
    return 13


def test_simple():
    n = fixt()
    assert n == 13
