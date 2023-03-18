from __future__ import annotations

import inspect
from dataclasses import dataclass, field
from enum import Enum
from typing import (
    Callable, Generic, Iterator, Literal, ParamSpec, TypeVar, overload,
)

from ._manager import defer
from ._scope import Scope


R = TypeVar('R')
P = ParamSpec('P')


class Sentinel(Enum):
    UNSET = object()


@dataclass
class Fixture(Generic[P, R]):
    _callback: Callable[P, R | Iterator[R]]
    scope: Scope = Scope.FUNCTION
    _iters: list[Iterator[R]] = field(default_factory=list)
    _result: R | Literal[Sentinel.UNSET] = Sentinel.UNSET

    @overload
    def __get__(self, obj: None, objtype) -> Fixture[P, R]:
        pass

    @overload
    def __get__(self, obj: object, objtype) -> R:
        pass

    def __get__(self, obj, objtype) -> Fixture[P, R] | R:
        if obj is None:
            return self
        return self.__call__()

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
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
        return self.setup()

    def __exit__(self, *exc_info) -> None:
        self.teardown()
