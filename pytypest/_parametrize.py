from __future__ import annotations

import inspect
from typing import TYPE_CHECKING, Callable, ParamSpec

import pytest

from ._case import Case


if TYPE_CHECKING:
    from _pytest.mark import ParameterSet

P = ParamSpec('P')


def parametrize(
    func: Callable[P, None],
    *cases: Case[P],
    **named_cases: Case[P],
) -> Callable[[], None]:
    """Create a test for each case, each test calling the given func.

    ::

        def _test_add(a: int, b: int, exp: int) -> None:
            assert a + b == exp

        test_add = parametrize(
            _test_add,
            case(3, 4, exp=7),
            case(4, 5, exp=9),
            zeros=case(0, 0, exp=0),
        )

    """
    sig = inspect.Signature.from_callable(func)
    params = list(sig.parameters)
    table: list[ParameterSet | list] = []
    row: ParameterSet | list
    all_cases = list(cases)
    for name, case in named_cases.items():
        all_cases.append(case.with_id(name))
    for case in all_cases:
        bound = sig.bind(*case.args, **case.kwargs)
        bound.apply_defaults()
        row = [bound.arguments[p] for p in params]
        if case.id or case.tags:
            marks = [getattr(pytest.mark, tag) for tag in (case.tags or [])]
            row = pytest.param(*row, id=case.id, marks=tuple(marks))
        table.append(row)
    func.__defaults__ = ()
    return pytest.mark.parametrize(params, table)(func)
