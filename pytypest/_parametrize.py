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
) -> Callable[[], None]:
    sig = inspect.Signature.from_callable(func)
    params = list(sig.parameters)
    table: list[ParameterSet | list] = []
    row: ParameterSet | list
    for case in cases:
        bound = sig.bind(*case.args, **case.kwargs)
        bound.apply_defaults()
        row = [bound.arguments[p] for p in params]
        if case.id or case.tags:
            marks = [getattr(pytest.mark, tag) for tag in (case.tags or [])]
            row = pytest.param(*row, id=case.id, marks=tuple(marks))
        table.append(row)
    func.__defaults__ = ()
    return pytest.mark.parametrize(params, table)(func)
