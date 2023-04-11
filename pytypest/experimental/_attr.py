from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Generic, TypeVar, overload

from typing_extensions import ParamSpec


if TYPE_CHECKING:
    from .._fixture import Fixture


P = ParamSpec('P')
R = TypeVar('R')


def attr(fixture: Fixture[P, R], *args: P.args, **kwargs: P.kwargs) -> Attr[P, R]:
    """A wrapper to use a fixture as a container attribute.

    A fixture wrapped with ``attr`` can be accessed as a class attribute
    without explicitly calling it. It's equivalent to defining a ``@property``
    that calls the fixture inside and returns its result but shorter.

    ::

        class Fixtures:
            user = attr(get_user)

        def test_user():
            f = Fixtures()
            assert f.user.name == 'mark'

    """
    return Attr(fixture, args, kwargs)


@dataclass(frozen=True)
class Attr(Generic[P, R]):
    fixture: Fixture[P, R]
    args: tuple
    kwargs: dict[str, Any]

    @overload
    def __get__(self, obj: None, objtype: type) -> Attr[P, R]:
        pass

    @overload
    def __get__(self, obj: object, objtype: type) -> R:
        pass

    def __get__(self, obj: object | None, objtype: type) -> Attr[P, R] | R:
        if obj is None:
            return self
        return self.fixture(*self.args, **self.kwargs)
