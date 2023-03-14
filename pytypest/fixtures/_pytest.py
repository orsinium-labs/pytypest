from __future__ import annotations
import os
from pathlib import Path

from typing import Any, Mapping
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
def capture_std(binary: bool = False) -> pytest.CaptureFixture:
    if binary:
        return get_pytest_fixture('capsysbinary')
    return get_pytest_fixture('capsys')


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
def monkeypatch() -> pytest.MonkeyPatch:
    return get_pytest_fixture('monkeypatch')


@fixture
def record_warnings() -> pytest.WarningsRecorder:
    return get_pytest_fixture('recwarn')


@fixture
def make_temp_dir(basename: str | None = None) -> Path:
    factory: pytest.TempPathFactory = get_pytest_fixture('tmp_path_factory')
    if basename is not None:
        return factory.mktemp(basename=basename)
    return factory.getbasetemp()


@fixture
def chdir(path: Path) -> None:
    monkeypatch().chdir(path)


@fixture
def update_environ(
    _new: dict[str, str] | None = None,
    **kwargs: str,
) -> Mapping[str, str]:
    patcher = monkeypatch()
    for name, value in (_new or {}).items():
        patcher.setenv(name, value)
    for name, value in kwargs.items():
        patcher.setenv(name, value)
    return os.environ
