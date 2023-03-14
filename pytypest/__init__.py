"""Type-safe and maintainable fixtures and parametrization for pytest.
"""

from ._fixture_factory import fixture
from ._parametrize import parametrize
from ._scope import Scope
from ._case import case

__version__ = '0.1.0'
__all__ = [
    'case',
    'fixture',
    'parametrize',
    'Scope',
]
