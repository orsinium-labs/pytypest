from __future__ import annotations

import os
import socket
import unittest.mock
from pathlib import Path
from typing import (
    Callable, ContextManager, Iterator, MutableMapping, Sequence, TypeVar,
)

from .._fixture_factory import fixture
from ._helpers import NetworkGuard


T = TypeVar('T', covariant=True)


@fixture
def defer(callback: Callable[[], None]) -> Iterator[None]:
    yield
    callback()


@fixture
def enter_context(manager: ContextManager[T]) -> Iterator[T]:
    with manager as value:
        yield value


@fixture
def forbid_networking(
    allowed_hosts: Sequence[str] = (),
    allowed_ports: Sequence[int] = (),
) -> Iterator[None]:
    guard = NetworkGuard(
        allowed_hosts=frozenset(allowed_hosts),
        allowed_ports=frozenset(allowed_ports),
        wrapped=socket.getaddrinfo,
    )
    socket.getaddrinfo = guard
    yield
    socket.getaddrinfo = guard.wrapped


@fixture
def chdir(path: Path) -> Iterator[None]:
    old_path = os.getcwd()
    os.chdir(path)
    yield
    os.chdir(old_path)


@fixture
def preserve_mapping(target: MutableMapping) -> Iterator[None]:
    with unittest.mock.patch.dict(target):
        yield
