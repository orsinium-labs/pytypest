from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest
    from ._manager import Manager


@dataclass
class Hub:
    manager: Manager | None = None
    request: pytest.FixtureRequest | None = None


hub = Hub()
