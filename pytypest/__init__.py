"""Type-safe and maintainable fixtures and parametrization for pytest.
"""

from . import fixtures
from ._autouse import autouse
from ._fixture_factory import fixture
from ._parametrize import parametrize
from ._scope import Scope
from ._case import case

__version__ = '0.1.0'
__all__ = [
    'autouse',
    'case',
    'fixture',
    'fixtures',
    'parametrize',
    'Scope',
]
