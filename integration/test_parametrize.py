from pytypest import parametrize, case


def _test_double(x: int, exp: int):
    assert x * 2 == exp


test_double = parametrize(
    _test_double,
    case(3, 6),
    case(3, exp=6),
    case(x=3, exp=6),
    case.id('pos-only')(3, 6),
)
