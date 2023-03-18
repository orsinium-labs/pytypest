from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from .._fixture_factory import fixture
from .._hub import hub


@fixture
def get_request() -> pytest.FixtureRequest:
    if hub.request is None:
        raise RuntimeError('pytest plugin is not active')
    return hub.request


@fixture
def get_pytest_fixture(name: str) -> Any:
    request = get_request()
    return request.getfixturevalue(name)


@fixture
def capture_std(*, binary: bool = False, fd: bool = False) -> pytest.CaptureFixture:
    """Capture stdout and stderr.
    """
    root = 'fd' if fd else 'sys'
    suffix = 'binary' if binary else ''
    return get_pytest_fixture(f'cap{root}{suffix}')


@fixture
def capture_logs() -> pytest.LogCaptureFixture:
    return get_pytest_fixture('caplog')


@fixture
def update_doctest_namespace(
    _new: dict[str, Any] | None = None,
    **kwargs: Any,
) -> dict[str, Any]:
    ns: dict = get_pytest_fixture('doctest_namespace')
    if _new:
        ns.update(_new)
    ns.update(kwargs)
    return ns


@fixture
def record_warnings() -> pytest.WarningsRecorder:
    return get_pytest_fixture('recwarn')


@fixture
def make_temp_dir(basename: str | None = None, numbered: bool = True) -> Path:
    factory: pytest.TempPathFactory = get_pytest_fixture('tmp_path_factory')
    if basename is not None:
        return factory.mktemp(basename=basename, numbered=numbered)
    return factory.getbasetemp()
