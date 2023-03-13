from __future__ import annotations
from typing import TYPE_CHECKING, Iterator
import pytest
from ._scope import Scope
from ._manager import Manager

if TYPE_CHECKING:
    from _pytest.fixtures import FixtureRequest
    from _pytest.main import Session


SESSION_ATTR = '_pytypest_manager'


def pytest_sessionstart(session: Session) -> None:
    manager = Manager()
    manager.set_as_global()
    setattr(session, SESSION_ATTR, manager)


def _manage_scope(request: FixtureRequest) -> Iterator[None]:
    manager: Manager = getattr(request.session, SESSION_ATTR)
    scope = Scope(request.scope)
    manager.enter_scope(scope)
    yield
    manager.exit_scope(scope)


enter_function = pytest.fixture(scope='function', autouse=True)(_manage_scope)
enter_class = pytest.fixture(scope='class', autouse=True)(_manage_scope)
enter_module = pytest.fixture(scope='module', autouse=True)(_manage_scope)
enter_package = pytest.fixture(scope='package', autouse=True)(_manage_scope)
enter_session = pytest.fixture(scope='session', autouse=True)(_manage_scope)
