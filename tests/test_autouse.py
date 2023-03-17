import pytest

from pytypest import Scope, autouse, fixture


def test_double_autouse(isolated) -> None:
    @fixture
    def fixt():
        yield

    autouse(fixt)
    msg = 'autouse can be called only once'
    with pytest.raises(RuntimeError, match=msg):
        autouse(fixt)


def test_autouse(isolated, scoped) -> None:
    log = []

    @fixture(scope=Scope.CLASS)
    def fixt():
        log.append('s')
        yield
        log.append('t')

    autouse(fixt)
    assert log == []
    with scoped('class'):
        assert log == ['s']
        with scoped('function'):
            assert log == ['s']
        assert log == ['s']
    assert log == ['s', 't']
