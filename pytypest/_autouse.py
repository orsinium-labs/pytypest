from __future__ import annotations

from typing import TYPE_CHECKING

from ._hub import hub


if TYPE_CHECKING:
    from ._fixture import Fixture


def autouse(*fixtures: Fixture[[], None]) -> None:
    """Register fixtures to be used automatically when entering a scope.

    Can be called only once in runtime.

    ::

        autouse(
            create_database,
            clear_cache,
            fixtures.forbid_networking,
        )

    """
    if hub.autouse is not None:
        raise RuntimeError('autouse can be called only once')
    hub.autouse = fixtures
