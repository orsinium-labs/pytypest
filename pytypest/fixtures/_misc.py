from __future__ import annotations

import socket
from dataclasses import dataclass
from typing import Callable, ContextManager, Iterator, Sequence, TypeVar

import pytest

from .._fixture_factory import fixture


T = TypeVar('T', covariant=True)


@fixture
def defer(callback: Callable[[], None]) -> Iterator[None]:
    yield
    callback()


@fixture
def enter_context(manager: ContextManager[T]) -> Iterator[T]:
    with manager as value:
        yield value


@dataclass(frozen=True)
class NetworkGuard:
    allowed_hosts: frozenset[str]
    allowed_ports: frozenset[int]
    wrapped: Callable[..., list]

    def __call__(
        self,
        host: bytes | str | None,
        port: bytes | str | int | None,
        *args, **kwargs
    ) -> list:
        if host not in self.allowed_hosts:
            pytest.fail('connection to the host is not allowed')
        if port not in self.allowed_ports:
            pytest.fail('connection to the port is not allowed')
        return self.wrapped(host, port, *args, **kwargs)


@fixture
def forbid_networking(
    allowed_hosts: Sequence[str],
    allowed_ports: Sequence[int],
) -> Iterator[None]:
    guard = NetworkGuard(
        allowed_hosts=frozenset(allowed_hosts),
        allowed_ports=frozenset(allowed_ports),
        wrapped=socket.getaddrinfo,
    )
    socket.getaddrinfo = guard
    yield
    socket.getaddrinfo = guard.wrapped
