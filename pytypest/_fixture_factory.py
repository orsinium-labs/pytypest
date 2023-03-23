from __future__ import annotations

from typing import TYPE_CHECKING, Protocol, overload

from ._fixture import Fixture
from ._scope import Scope


if TYPE_CHECKING:
    from typing import Callable, Iterator, Literal, ParamSpec, TypeVar

    R = TypeVar('R')
    P = ParamSpec('P')


class FixtureMaker(Protocol):
    """
    The type of the callback returned by the @fixture
    when the decorator is called without the wrapped function
    and it has a function scope.
    """
    @overload
    def __call__(self, callback: Callable[P, Iterator[R]]) -> Fixture[P, R]:
        pass

    @overload
    def __call__(self, callback: Callable[P, R]) -> Fixture[P, R]:
        pass

    def __call__(self, callback):
        pass


class FixtureMakerWithScope(Protocol):
    """
    The type of the callback returned by the @fixture
    when non-function `scope` is passed.

    For non-function scope, fixtures must not accept arguments.
    The reason is that it cannot be properly cached.
    """
    @overload
    def __call__(self, callback: Callable[[], Iterator[R]]) -> Fixture[[], R]:
        pass

    @overload
    def __call__(self, callback: Callable[[], R]) -> Fixture[[], R]:
        pass

    def __call__(self, callback):
        pass


@overload
def fixture(
    callback: None = None,
    *,
    scope: Literal[Scope.FUNCTION] = Scope.FUNCTION,
) -> FixtureMaker:
    """fixture decorator with explicit function scope.

    ::
        @fixture(scope=Scope.FUNCTION)
        def get_user():
            return User()

    """
    pass


@overload
def fixture(
    callback: None = None,
    *,
    scope: Scope,
) -> FixtureMakerWithScope:
    """fixture decorator with scope.

    ::

        @fixture(scope=Scope.SESSION)
        def get_user():
            return User()

    """
    pass


@overload
def fixture(callback: Callable[P, Iterator[R]]) -> Fixture[P, R]:
    """fixture decorator with teardown without scope.

    ::

        @fixture
        def get_user():
            yield User()

    """
    pass


@overload
def fixture(callback: Callable[P, R]) -> Fixture[P, R]:
    """fixture decorator without teardown without scope.

    ::

        @fixture
        def get_user():
            return User()

    """
    pass


def fixture(callback: Callable | None = None, **kwargs) -> Fixture[P, R] | Callable:
    """A decorator to create a new fixture.

    Fixtures are executed only when called, cached for the given scope,
    and may have tear down logic that is executed when exiting the scope.

    ::

        @fixture
        def get_user() -> Iterator[User]:
            # setup
            u = User()
            # fixtures can use other fixtures
            db = get_database()
            db.insert(u)

            # provide data for the test
            yield u

            # teardown
            db.delete(u)

        def test_user():
            u = get_user()
            ...

    """
    if callback is not None:
        return Fixture(callback, **kwargs)

    def wrapper(callback):
        return Fixture(callback, **kwargs)
    return wrapper
