from __future__ import annotations
import os

from pathlib import Path
from typing import Iterator, Mapping
import unittest.mock

import pytest

from .._fixture_factory import fixture


@fixture
def monkeypatch() -> Iterator[pytest.MonkeyPatch]:
    patcher = pytest.MonkeyPatch()
    yield patcher
    patcher.undo()


@fixture
def chdir(path: Path) -> Iterator[None]:
    old_path = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(old_path)


@fixture
def update_environ(
    _new: dict[str, str | None] | None = None,
    **kwargs: str | None,
) -> Iterator[Mapping[str, str]]:
    patcher = pytest.MonkeyPatch()
    for name, value in (_new or {}).items():
        if value is None:
            patcher.delenv(name)
        else:
            patcher.setenv(name, value)
    for name, value in kwargs.items():
        if value is None:
            patcher.delenv(name)
        else:
            patcher.setenv(name, value)
    yield os.environ
    patcher.undo()


def setattr(*args, **kwargs) -> Iterator[None]:
    patcher = pytest.MonkeyPatch()
    patcher.setattr(*args, **kwargs)
    yield
    patcher.undo()


@fixture
def mock(target: str | None = None, **kwargs) -> Iterator[unittest.mock.Mock]:
    mock = unittest.mock.Mock(**kwargs)
    if not target:
        yield mock
        return

    with unittest.mock.patch(target, mock):
        yield mock
