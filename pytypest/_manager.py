from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable
from ._scope import Scope
from ._scope_manager import ScopeManager

_manager: Manager | None = None


def defer(callback: Callable[[], None]) -> None:
    global _manager
    assert _manager is not None, 'Manager must be used from test session'
    scope_manager = _manager._scopes[-1]
    scope_manager.defer(callback)


@dataclass
class Manager:
    _scopes: list[ScopeManager] = field(default_factory=list)

    def set_as_global(self) -> None:
        global _manager
        _manager = self

    def enter_scope(self, scope: Scope) -> None:
        if not self._scopes:
            assert scope == Scope.SESSION
        # else:
        #     assert self._scopes[-1].scope > scope
        scope_manager = ScopeManager(scope)
        self._scopes.append(scope_manager)

    def exit_scope(self, scope: Scope) -> None:
        scope_manager = self._scopes.pop()
        assert scope_manager.scope == scope
        scope_manager.exit_scope()
