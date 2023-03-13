from pytypest import fixture


@fixture
def fixt() -> int:
    return 13


def test_simple():
    n = fixt()
    assert n == 13
