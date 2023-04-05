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
    """Execute the given callback when leaving the test function.

    It's a nice way to clean up after a test function without
    creating a fixture or a context manager.
    """
    yield
    callback()


@fixture
def enter_context(manager: ContextManager[T]) -> Iterator[T]:
    """
    Enter the context manager, return its result,
    and exit the context when leaving the test function.

    It's a bit imilar to `contextlib.ExitStack` in a sense
    that it helps to keep code indentation low
    when entering multiple context managers.
    """
    with manager as value:
        yield value


@fixture
def forbid_networking(
    *,
    allowed: Sequence[tuple[str, int]] = (),
) -> Iterator[None]:
    """Forbid network connections during the test.

    This fixture is a good candidate for :func:`pytypest.autouse`.

    You can specify exceptions with `allowed_hosts` and `allowed_ports`
    """
    guard = NetworkGuard(
        allowed=frozenset(allowed),
        wrapped=socket.getaddrinfo,
    )
    socket.getaddrinfo = guard
    yield
    socket.getaddrinfo = guard.wrapped


@fixture
def chdir(path: Path) -> Iterator[None]:
    old_path = Path.cwd()
    os.chdir(path)
    yield
    os.chdir(old_path)


@fixture
def preserve_mapping(target: MutableMapping) -> Iterator[None]:
    with unittest.mock.patch.dict(target):
        yield
