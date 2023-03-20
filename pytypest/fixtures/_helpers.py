from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import pytest


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
