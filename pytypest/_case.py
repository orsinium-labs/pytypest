from __future__ import annotations

import dataclasses
from typing import Any, Generic, ParamSpec, TypeVar


P = ParamSpec('P')
S = TypeVar('S')


@dataclasses.dataclass(frozen=True)
class CaseMaker:
    """Create a new test case to be used with parametrized tests.

    ::

        def _test_add(a: int, b: int, exp: int):
            assert a + b == exp

        test_add = parametrize(
            _test_add,
            case(4, 5, exp=9),
        )

    """
    _id: str | None = None
    _tags: tuple[str, ...] | None = None

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> Case[P]:
        return Case(args=args, kwargs=kwargs, id=self._id, tags=self._tags)

    def id(self, id: str) -> CaseMaker:
        """Give a name to the test case.

        ::

            test_logout = parametrize(
                _test_logout,
                case.id('anonymous_user')(user1),
            )

        """
        return dataclasses.replace(self, _id=id)

    def tags(self, *tags: str) -> CaseMaker:
        """Mark the case with tags that can be used to filter specific tests.

        ::

            test_logout = parametrize(
                _test_logout,
                case.tags('slow', 'integration')(user1),
            )

        """
        return dataclasses.replace(self, _tags=tags)


case = CaseMaker()


@dataclasses.dataclass(frozen=True)
class Case(Generic[P]):
    """A single test case for parametrized tests.

    Use :func:`pytypest.case` to create a new one.
    """
    args: tuple
    kwargs: dict[str, Any]
    id: str | None = None
    tags: tuple[str, ...] | None = None

    def with_id(self, id: str) -> Case[P]:
        return dataclasses.replace(self, id=id)
