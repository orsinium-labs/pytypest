from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable
from ._scope import Scope
from ._scope_manager import ScopeManager
from ._hub import hub


def defer(scope: Scope, callback: Callable[[], None]) -> None:
    if hub.manager is None:
        raise RuntimeError('pytest plugin is not activated')
    scope_manager = hub.manager.get_scope(scope)
    scope_manager.defer(callback)


@dataclass
class Manager:
    _scopes: list[ScopeManager] = field(default_factory=list)

    def get_scope(self, scope: Scope) -> ScopeManager:
        for scope_manager in self._scopes:
            if scope_manager.scope is scope:
                return scope_manager
        raise LookupError(f'cannot find ScopeManager for `{scope.value}` scope')

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
