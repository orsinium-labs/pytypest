from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Generic, Iterator, Literal, ParamSpec, TypeVar

from ._manager import defer
from ._scope import Scope


R = TypeVar('R')
P = ParamSpec('P')


class Sentinel(Enum):
    """A helper to define a singleton sentinel object in a mypy-friendly way.

    ::

        _: Literal[Sentinel.UNSET] = Sentinel.UNSET

    """
    UNSET = object()


@dataclass
class Fixture(Generic[P, R]):
    """A test fixture with setup and optional teardown.

    Should be constructed using :func:`pytypest.fixture`::

        @fixture
        def get_user() -> Iterator[User]:
            ... # setup
            yield User()
            ... # teardown

    """
    _callback: Callable[P, R | Iterator[R]]
    scope: Scope = Scope.FUNCTION
    _iters: list[Iterator[R]] = field(default_factory=list)
    _result: R | Literal[Sentinel.UNSET] = Sentinel.UNSET

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        """Allows the fixture to be called as a function.

        ::

            @fixture
            def get_user():
                ...

            user = get_user()

        """
        if self.scope != Scope.FUNCTION:
            msg = 'fixtures with non-function scope must not accept arguments'
            assert not args and not kwargs, msg
        is_cached = self._result != Sentinel.UNSET and not args and not kwargs
        if is_cached:
            return self._result  # type: ignore[return-value]
        result = self.setup(*args, **kwargs)
        defer(self.scope, self.teardown)
        return result

    def setup(self, *args: P.args, **kwargs: P.kwargs) -> R:
        """Execute setup logic of the fixture and get its result.

        Setup is everything that goes before `yield` or `return`.

        Avoid using this method directly. It doesn't use cached results,
        doesn't use the scope, and doesn't defer teardown.
        Prefer calling the fixture or using it as a context manager.
        """
        if inspect.isgeneratorfunction(self._callback):
            iterator = self._callback(*args, **kwargs)
            result = next(iterator)
            self._iters.append(iterator)
        else:
            result = self._callback(*args, **kwargs)
        if not args and not kwargs:
            self._result = result
        return result

    def teardown(self) -> None:
        """Execute teardown logic of the fixture (if available).

        Teardown is the code that goes after `yield` (if `yield` is present).

        Can be safely called mutiple times.
        """
        for iterator in self._iters:
            try:
                next(iterator)
            except StopIteration:
                pass
            else:
                raise RuntimeError('fixture must have at most one yield')
        self._iters = []
        self._result = Sentinel.UNSET

    def __enter__(self) -> R:
        """Allows the fixture to be used as a context manager.

        ::

            @fixture
            def get_user():
                ...

            with get_user as user:
                ...

        Regardless of the scope, the setup is executed when entering
        the context, and the teardown is when leaving it.

        """
        return self.setup()

    def __exit__(self, *exc_info) -> None:
        self.teardown()
