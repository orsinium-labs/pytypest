from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import pytest


@dataclass(frozen=True)
class NetworkGuard:
    allowed: frozenset[tuple[str, int]]
    wrapped: Callable[..., list]

    def __call__(
        self,
        host: bytes | str | None,
        port: bytes | str | int | None,
        *args,
        **kwargs,
    ) -> list:
        if (host, port) not in self.allowed:
            msg = f'connection to {host}:{port} is not allowed'  # type: ignore
            pytest.fail(msg)
        return self.wrapped(host, port, *args, **kwargs)
