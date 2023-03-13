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

    def __call__(self, *args: P.args, **kwargs: P.kwargs):
        if self.scope != Scope.FUNCTION:
            if args or kwargs:
                msg = 'fixtures with non-function scope must not accept arguments'
                raise ValueError(msg)
        defer(self.scope, self.teardown)
        return self.setup(*args, **kwargs)

    def setup(self, *args: P.args, **kwargs: P.kwargs) -> R:
        if self._result is Sentinel.UNSET:
            self._iter = None
            if inspect.isgeneratorfunction(self._callback):
                self._iter = self._callback(*args, **kwargs)
                self._result = next(self._iter)
            else:
                self._result = self._callback(*args, **kwargs)  # type: ignore[assignment]
        return self._result  # type: ignore[return-value]

    def teardown(self) -> None:
        if self._iter is not None:
            try:
                next(self._iter)
            except StopIteration:
                pass
            self._iter = None
        self._result = Sentinel.UNSET
