from __future__ import annotations

from contextlib import contextmanager
from typing import Callable, Iterator

import pytest

from pytypest import _plugin
from pytypest._hub import hub


@pytest.fixture
def isolated(request: pytest.FixtureRequest) -> Iterator[None]:
    _plugin.pytest_sessionstart(request.session)
    yield
    hub.reset()
    delattr(request.session, _plugin.SESSION_ATTR)


@pytest.fixture
def scoped(request: pytest.FixtureRequest) -> Iterator[Callable]:

    @contextmanager
    def wrapper(scope: str):
        from _pytest.scope import Scope

        old_scope = request._scope
        request._scope = Scope(scope)
        it = _plugin._manage_scope(request)
        next(it)
        try:
            yield
        finally:
            try:
                next(it)
            except StopIteration:
                pass
            request._scope = old_scope

    yield wrapper
