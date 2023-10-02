"""Type-safe and maintainable fixtures and parametrization for pytest.
"""

from . import experimental, fixtures
from ._autouse import autouse
from ._case import case
from ._fixture_factory import fixture
from ._parametrize import parametrize
from ._scope import Scope


__version__ = '1.0.1'
__all__ = [
    'autouse',
    'case',
    'experimental',
    'fixture',
    'fixtures',
    'parametrize',
    'Scope',
]
