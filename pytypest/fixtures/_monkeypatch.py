from __future__ import annotations

import os
import unittest.mock
from pathlib import Path
from typing import Iterator, Mapping, MutableMapping

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


@fixture
def preserve_mapping(target: MutableMapping) -> Iterator[None]:
    with unittest.mock.patch.dict(target):
        yield
