from __future__ import annotations

from pytypest import experimental


def test_setattr(isolated, scoped):
    class A:
        a = 13

    with scoped('function'):
        p = experimental.patcher(A)
        p.a = 54
        assert A.a == 54
    assert A.a == 13


def test_delattr(isolated, scoped):
    class A:
        a = 13

    with scoped('function'):
        p = experimental.patcher(A)
        del p.a
        assert not hasattr(A, 'a')
    assert A.a == 13


def test_setitem(isolated, scoped):
    a = {'b': 1}
    with scoped('function'):
        p = experimental.item_patcher(a)
        assert a == {'b': 1}
        p['b'] = 2
        p['c'] = 3
        assert a == {'b': 2, 'c': 3}
    assert a == {'b': 1}


def test_delitem(isolated, scoped):
    a = {'b': 1, 'c': 2}
    with scoped('function'):
        p = experimental.item_patcher(a)
        assert a == {'b': 1, 'c': 2}
        del p['c']
        assert a == {'b': 1}
    assert a == {'b': 1, 'c': 2}
