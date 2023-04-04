from typing import Callable

import pytest

from pytypest import Scope, fixture


def test_setup_return() -> None:
    log = []

    @fixture
    def fixt():
        log.append(42)
        return 13

    assert fixt.setup() == 13
    assert log == [42]


def test_setup_yield() -> None:
    log = []

    @fixture
    def fixt():
        log.append(42)
        yield 13

    assert fixt.setup() == 13
    assert log == [42]


def test_teardown_return() -> None:
    @fixture
    def fixt():
        return 13

    fixt.teardown()
    assert fixt.setup() == 13
    fixt.teardown()


def test_teardown_yield() -> None:
    log = []

    @fixture
    def fixt():
        yield 13
        log.append(42)

    fixt.teardown()
    assert fixt.setup() == 13
    fixt.teardown()
    assert log == [42]


def test_teardown_on_leaving_scope(isolated: None, scoped: Callable) -> None:
    log = []

    @fixture(scope=Scope.CLASS)
    def fixt():
        log.append('s')
        yield 62
        log.append('t')

    with scoped('class'):
        with scoped('function'):
            assert log == []
            for _ in range(4):
                assert fixt() == 62
                assert log == ['s']
        assert log == ['s']

    assert log == ['s', 't']


def test_disallow_double_yield(isolated, scoped):
    @fixture
    def fixt():
        yield
        yield

    msg = 'fixture must have at most one yield'
    with pytest.raises(RuntimeError, match=msg):
        with scoped('function'):
            fixt()


def test_plugin_not_active():
    @fixture
    def fixt():
        yield

    msg = 'pytest plugin is not activated'
    with pytest.raises(RuntimeError, match=msg):
        fixt()


def test_context_manager(isolated, scoped):
    log = []

    @fixture
    def fixt():
        log.append('s')
        yield 67
        log.append('t')

    with scoped('function'):
        assert log == []
        with fixt as val:
            assert log == ['s']
            assert val == 67
        assert log == ['s', 't']
    assert log == ['s', 't']
