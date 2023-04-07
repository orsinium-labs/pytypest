from __future__ import annotations

from pathlib import Path
from typing import Any, Iterator

import pytest

from .._fixture_factory import fixture
from .._hub import hub


@fixture
def get_request() -> pytest.FixtureRequest:
    """Get meta information about the currently running test.

    A wrapper around :pytest:`request` pytest fixture.

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

    A wrapper around :pytest:`pytest.FixtureRequest.getfixturevalue`.

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

    A wrapper around :pytest:`capsys`, :pytest:`capfd`, :pytest:`capsysbinary`,
    and :pytest:`capfdbinary` pytest fixtures.

    ::

        cap = capture_std()
        print('hello')
        captured = cap.readouterr()
        assert captured.out.rstrip() == 'hello'

    """
    root = 'fd' if fd else 'sys'
    suffix = 'binary' if binary else ''
    return get_pytest_fixture(f'cap{root}{suffix}')


@fixture
def capture_logs() -> pytest.LogCaptureFixture:
    """Capture all log records.

    A wrapper around :pytest:`caplog` pytest fixture.

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

    A wrapper around :pytest:`recwarn` pytest fixture.

    ::

        import warnings
        rec = fixtures.record_warnings()
        warnings.warn('oh hi mark', UserWarning)
        w = rec.pop(UserWarning)
        assert str(w.message) == 'oh hi mark'

    """
    return get_pytest_fixture('recwarn')


@fixture
def make_temp_dir(basename: str | None = None, numbered: bool = True) -> Path:
    """Create a temporary directory.

    A wrapper around :pytest:`tmp_path` and :pytest:`tmp_path_factory`
    pytest fixtures.

    Args:
        basename: if specified, the created directory will have this name.
        numbered: if True (default), ensure the directory is unique
            by adding a numbered suffix greater than any existing one.

    ::

        dir_path = fixtures.make_temp_dir()
        file_path = dir_path / 'example.py'
        file_path.write_text('1 + 2')
        ...
        content = file_path.read_text()
        assert content == '1 + 2'

    """
    if basename is not None:
        factory: pytest.TempPathFactory = get_pytest_fixture('tmp_path_factory')
        return factory.mktemp(basename=basename, numbered=numbered)
    return get_pytest_fixture('tmp_path')


@fixture
def monkeypatch() -> Iterator[pytest.MonkeyPatch]:
    """Patch attributes of objects for the duration of test.

    A wrapper around :pytest:`monkeypatch` pytest fixture.

    Usually, you don't need to use this fixture directly. The preferred way to
    patch things is using :func:`pytypest.fixtures.setattr`,
    :func:`pytypest.fixtures.delattr`, and :func:`pytypest.fixtures.preserve_mapping`.
    """
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
    """Patch an attribute for the duration of test.

    A wrapper around :pytest:`pytest.MonkeyPatch.setattr`.

    The target can be either the object to patch or the full import path to the object.
    The target can be any object, including modules, classes, methods, and functions.

    ::

        from unittest.mock import Mock
        mock = Mock()
        setattr('logging', 'info', mock)

    """
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
    """Delete attribute of an object for the duration of test.

    A wrapper around :pytest:`pytest.MonkeyPatch.delattr`.

    The target can be either the object to patch or the full import path to the object.
    The target can be any object, including modules, classes, methods, and functions.

    ::

        delattr(logging, 'info')

    """
    patcher = pytest.MonkeyPatch()
    if isinstance(target, str):
        patcher.delattr(f'{target}.{name}', raising=must_exist)
    else:
        patcher.delattr(target, name, raising=must_exist)
    yield
    patcher.undo()
