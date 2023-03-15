from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    import pytest
    from ._manager import Manager
    from ._fixture import Fixture


@dataclass
class Hub:
    """Singleton holding all global state.
    """
    manager: Manager | None = None
    request: pytest.FixtureRequest | None = None
    autouse: tuple[Fixture[[], None], ...] | None = None


hub = Hub()
