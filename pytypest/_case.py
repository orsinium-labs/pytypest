from __future__ import annotations

import dataclasses
from typing import Generic, ParamSpec, TypeVar


P = ParamSpec('P')
S = TypeVar('S')


@dataclasses.dataclass(frozen=True)
class CaseMaker:
    _id: str | None = None
    _tags: tuple[str, ...] | None = None

    def __call__(self, *args: P.args, **kwargs: P.kwargs) -> Case[P]:
        return Case(args=args, kwargs=kwargs, id=self._id, tags=self._tags)

    def id(self, id: str) -> CaseMaker:
        return dataclasses.replace(self, _id=id)

    def tags(self, *tags: str) -> CaseMaker:
        return dataclasses.replace(self, _tags=tags)


case = CaseMaker()


@dataclasses.dataclass(frozen=True)
class Case(Generic[P]):
    args: tuple
    kwargs: dict
    id: str | None = None
    tags: tuple[str, ...] | None = None
