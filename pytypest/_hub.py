from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    import pytest

    from ._fixture import Fixture
    from ._manager import Manager


@dataclass
class Hub:
    """Singleton holding all global state.
    """
    manager: Manager | None = None
    request: pytest.FixtureRequest | None = None
    autouse: tuple[Fixture[[], None], ...] | None = None

    def reset(self) -> None:
        """Clean up all global state.

        Used for pytypest's unit tests' isolation.
        """
        self.manager = None
        self.request = None
        self.autouse = None


hub = Hub()
