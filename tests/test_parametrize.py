from __future__ import annotations

from typing import TYPE_CHECKING

import pytest

from pytypest import case, parametrize


if TYPE_CHECKING:
    from _pytest.mark.structures import Mark


def test_parametrize() -> None:
    def inner(a: int, b: int):
        pass
    wrapped = parametrize(
        inner,
        case(3, 4),
        case(5, b=6),
        case(a=7, b=8),
        case(b=10, a=9),
        case.id('one')(11, 12),
        case.tags('two', 'three')(13, 14),
        four=case(15, 16),
    )
    mark: Mark
    (mark,) = wrapped.pytestmark  # type: ignore[attr-defined]
    assert mark.name == 'parametrize'
    assert mark.args == (
        ['a', 'b'],
        [
            [3, 4], [5, 6], [7, 8], [9, 10],
            pytest.param(11, 12, id='one'),
            pytest.param(13, 14, marks=(pytest.mark.two, pytest.mark.three)),
            pytest.param(15, 16, id='four'),
        ],
    )


def test_preserve_marks() -> None:
    @pytest.mark.two
    def inner(a: int, b: int):
        pass
    wrapped = parametrize(inner, case(3, 4))
    wrapped = pytest.mark.three(wrapped)
    marks = wrapped.pytestmark  # type: ignore[attr-defined]
    assert len(marks) == 3
