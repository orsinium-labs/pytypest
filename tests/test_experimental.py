from __future__ import annotations

from pytypest import experimental


class Global:
    attr: int = 42


def test_setattr(isolated, scoped):
    class A:
        a = 13

    with scoped('function'):
        p = experimental.patcher(A)
        p.a = 54
        assert A.a == 54
    assert A.a == 13


def test_setattr__str_target(isolated, scoped):
    target = f'{Global.__module__}.{Global.__name__}'
    with scoped('function'):
        p = experimental.patcher(target)
        p.attr = 99
        assert Global.attr == 99
    assert Global.attr == 42


def test_delattr(isolated, scoped):
    class A:
        a = 13

    with scoped('function'):
        p = experimental.patcher(A)
        del p.a
        assert not hasattr(A, 'a')
    assert A.a == 13
