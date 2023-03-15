from __future__ import annotations
from enum import Enum

import inspect
from dataclasses import dataclass
from typing import Callable, Generic, Iterator, Literal, ParamSpec, TypeVar, overload
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
    _iter: Iterator[R] | None = None
    _result: R | Literal[Sentinel.UNSET] = Sentinel.UNSET

    @overload
    def __get__(self, obj: None, objtype) -> Fixture[P, R]:
        ...

    @overload
    def __get__(self, obj: object, objtype) -> R:
        ...

    def __get__(self, obj, objtype) -> Fixture[P, R] | R:
        if obj is None:
            return self
        return self.__call__()

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> R:
        if self.scope != Scope.FUNCTION:
            if args or kwargs:
                msg = 'fixtures with non-function scope must not accept arguments'
                raise ValueError(msg)
        is_cached = self._result != Sentinel.UNSET and not args and not kwargs
        if is_cached:
            return self._result  # type: ignore[return-value]
        result = self.setup(*args, **kwargs)
        defer(self.scope, self.teardown)
        return result

    def setup(self, *args: P.args, **kwargs: P.kwargs) -> R:
        self._iter = None
        if inspect.isgeneratorfunction(self._callback):
            self._iter = self._callback(*args, **kwargs)
            result = next(self._iter)
        else:
            result = self._callback(*args, **kwargs)  # type: ignore[assignment]
        if not args and not kwargs:
            self._result = result
        return result

    def teardown(self) -> None:
        if self._iter is not None:
            try:
                next(self._iter)
            except StopIteration:
                pass
            else:
                raise RuntimeError('fixture must have at most one yield')
            self._iter = None
        self._result = Sentinel.UNSET
