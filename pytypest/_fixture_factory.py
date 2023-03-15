from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, overload

from ._fixture import Fixture
from ._scope import Scope


if TYPE_CHECKING:
    from typing import Callable, Iterator, Literal, ParamSpec, TypeVar

    R = TypeVar('R')
    P = ParamSpec('P')


class FixtureMaker(Protocol):
    @overload
    def __call__(self, callback: Callable[P, Iterator[R]]) -> Fixture[P, R]:
        ...

    @overload
    def __call__(self, callback: Callable[P, R]) -> Fixture[P, R]:
        ...

    def __call__(self, callback):
        ...


class FixtureMakerWithScope(Protocol):
    """
    The type of the callback returned by the @fixture
    when non-function `scope` is passed.

    For non-function scope, fixtures must not accept arguments.
    The reason is that it cannot be properly cached.
    """
    @overload
    def __call__(self, callback: Callable[[], Iterator[R]]) -> Fixture[[], R]:
        ...

    @overload
    def __call__(self, callback: Callable[[], R]) -> Fixture[[], R]:
        ...

    def __call__(self, callback):
        ...


@overload
def fixture(
    callback: None = None,
    *,
    scope: Literal[Scope.FUNCTION] = Scope.FUNCTION,
) -> FixtureMaker:
    pass


@overload
def fixture(
    callback: None = None,
    *,
    scope: Scope,
) -> FixtureMakerWithScope:
    pass


@overload
def fixture(callback: Callable[P, Iterator[R]]) -> Fixture[P, R]:
    pass


@overload
def fixture(callback: Callable[P, R]) -> Fixture[P, R]:
    pass


def fixture(callback: Callable | None = None, **kwargs) -> Fixture[P, R] | Callable:
    def wrapper(callback):
        return Fixture(callback, **kwargs)
    if callback is not None:
        return Fixture(callback, **kwargs)
    return wrapper
