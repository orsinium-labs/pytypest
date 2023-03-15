from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field
from typing import Callable

from ._scope import Scope


Finalizer = Callable[[], None]


@dataclass
class ScopeManager:
    scope: Scope
    _deferred: deque[Finalizer] = field(default_factory=deque)

    def defer(self, callback: Finalizer) -> None:
        self._deferred.append(callback)

    def enter_scope(self) -> None:
        assert not self._deferred

    def exit_scope(self) -> None:
        while self._deferred:
            callback = self._deferred.pop()
            callback()
