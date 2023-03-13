"""Type-safe and maintainable fixtures and parametrization for pytest.
"""

from ._fixture_factory import fixture
from ._scope import Scope

__version__ = '0.1.0'
__all__ = [
    'fixture',
    'Scope',
]
