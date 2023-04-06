from __future__ import annotations

from pathlib import Path
from typing import Any, Iterator

import pytest

from .._fixture_factory import fixture
from .._hub import hub


@fixture
def get_request() -> pytest.FixtureRequest:
    """Get meta information about the currently running test.

    A wrapper around ``request`` pytest fixture.

    ::

        request = get_request()
        verbosity = request.config.getoption("verbose")
        if verbosity > 0:
            ...

    """
    if hub.request is None:
        raise RuntimeError('pytest plugin is not active')
    return hub.request


@fixture
def get_pytest_fixture(name: str) -> Any:
    """Get a pytest fixture by its name.

    This is useful for using fixtures from third-party pytest plugins.
    All built-in pytest fixtures already have a convenient wrapper in pytypest.

    For example, get ``event_loop`` fixture from pytest-asyncio::

        from asyncio import AbstractEventLoop
        loop: AbstractEventLoop = get_pytest_fixture('event_loop')

    """
    request = get_request()
    return request.getfixturevalue(name)


@fixture
def capture_std(*, binary: bool = False, fd: bool = False) -> pytest.CaptureFixture:
    """Capture stdout and stderr.

    A wrapper around ``capsys``, ``capfd``, ``capsysbinary``, and ``capfdbinary``
    pytest fixtures.

    ::

        cap = capture_std()
        print("hello")
        captured = cap.readouterr()
        assert captured.out == "hello\n"

    """
    root = 'fd' if fd else 'sys'
    suffix = 'binary' if binary else ''
    return get_pytest_fixture(f'cap{root}{suffix}')


@fixture
def capture_logs() -> pytest.LogCaptureFixture:
    """Capture all log records.

    A wrapper around ``caplog`` pytest fixture.

    ::

        import logging
        cap = capture_logs()
        logging.warning('oh hi mark')
        record = cap.records[-1]
        assert record.message == 'oh hi mark'

    """
    return get_pytest_fixture('caplog')


@fixture
def record_warnings() -> pytest.WarningsRecorder:
    """Record all warnings (emitted using ``warnings`` module).

    A wrapper around ``recwarn`` pytest fixture.
    """
    return get_pytest_fixture('recwarn')


@fixture
def make_temp_dir(basename: str | None = None, numbered: bool = True) -> Path:
    factory: pytest.TempPathFactory = get_pytest_fixture('tmp_path_factory')
    if basename is not None:
        return factory.mktemp(basename=basename, numbered=numbered)
    return factory.getbasetemp()


@fixture
def monkeypatch() -> Iterator[pytest.MonkeyPatch]:
    patcher = pytest.MonkeyPatch()
    yield patcher
    patcher.undo()


@fixture
def setattr(
    target: object | str,
    name: str,
    value: object,
    *,
    must_exist: bool = True,
) -> Iterator[None]:
    patcher = pytest.MonkeyPatch()
    if isinstance(target, str):
        patcher.setattr(f'{target}.{name}', value, raising=must_exist)
    else:
        patcher.setattr(target, name, value, raising=must_exist)
    yield
    patcher.undo()


@fixture
def delattr(
    target: object | str,
    name: str,
    *,
    must_exist: bool = True,
) -> Iterator[None]:
    """Delete attribute of an object.
    """
    patcher = pytest.MonkeyPatch()
    if isinstance(target, str):
        patcher.delattr(f'{target}.{name}', raising=must_exist)
    else:
        patcher.delattr(target, name, raising=must_exist)
    yield
    patcher.undo()
