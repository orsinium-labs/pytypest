from __future__ import annotations
from typing import TYPE_CHECKING
from pytypest import parametrize, case
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
    )
    mark: Mark
    (mark,) = wrapped.pytestmark  # type: ignore[attr-defined]
    assert mark.name == 'parametrize'
    assert mark.args == (
        ['a', 'b'],
        [[3, 4], [5, 6], [7, 8], [9, 10]],
    )
