"""The basic test for `parametrize` and `case`.
"""
from pytypest import case, parametrize


def _test_double(x: int, exp: int):
    assert x * 2 == exp


test_double = parametrize(
    _test_double,
    case(3, 6),
    case(3, exp=6),
    case(x=3, exp=6),
    case.id('pos-only')(3, 6),
)


def _test_divide(x: int, y: int = 1, *, exp: int):
    assert x // y == exp


test_divide = parametrize(
    _test_divide,
    case(8, 2, exp=4),
    case(3, exp=3),
)
