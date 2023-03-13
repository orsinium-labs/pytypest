from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import Callable, Generic, Iterator, ParamSpec, TypeVar, overload
from ._manager import defer

R = TypeVar('R')
P = ParamSpec('P')


@overload
def fixture(callback: Callable[P, Iterator[R]]) -> Fixture[P, R]:
    pass


@overload
def fixture(callback: Callable[P, R]) -> Fixture[P, R]:
    pass


def fixture(callback: Callable[P, R | Iterator[R]]) -> Fixture[P, R]:
    return Fixture(callback)


@dataclass
class Fixture(Generic[P, R]):
    _callback: Callable[P, R | Iterator[R]]
    _iter: Iterator[R] | None = None

    def __get__(self, obj, objtype) -> R:
        if obj is None:
            return self  # type: ignore[return-value]
        return self.__call__()

    def __call__(self, *args: P.args, **kwargs: P.kwargs):
        defer(self.teardown)
        return self.setup(*args, **kwargs)

    def setup(self, *args: P.args, **kwargs: P.kwargs) -> R:
        if inspect.isgeneratorfunction(self._callback):
            self._iter = self._callback(*args, **kwargs)
            return next(self._iter)
        return self._callback(*args, **kwargs)  # type: ignore[return-value]

    def teardown(self) -> None:
        if self._iter is not None:
            try:
                next(self._iter)
            except StopIteration:
                pass
            self._iter = None
