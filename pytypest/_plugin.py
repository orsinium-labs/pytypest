from __future__ import annotations
from typing import TYPE_CHECKING, Iterator
import pytest
from ._scope import Scope
from ._manager import Manager
from ._hub import hub

if TYPE_CHECKING:
    from _pytest.fixtures import FixtureRequest
    from _pytest.main import Session


SESSION_ATTR = '_pytypest_manager'


def pytest_sessionstart(session: Session) -> None:
    manager = Manager()
    hub.manager = manager
    setattr(session, SESSION_ATTR, manager)


def _manage_scope(request: FixtureRequest) -> Iterator[None]:
    hub.request = request
    manager: Manager = getattr(request.session, SESSION_ATTR)
    scope = Scope(request.scope)
    manager.enter_scope(scope)
    yield
    manager.exit_scope(scope)
    hub.request = None


enter_function = pytest.fixture(scope='function', autouse=True)(_manage_scope)
enter_class = pytest.fixture(scope='class', autouse=True)(_manage_scope)
enter_module = pytest.fixture(scope='module', autouse=True)(_manage_scope)
enter_package = pytest.fixture(scope='package', autouse=True)(_manage_scope)
enter_session = pytest.fixture(scope='session', autouse=True)(_manage_scope)
