from __future__ import annotations
import dataclasses
from typing import Callable, Generic, ParamSpec


P = ParamSpec('P')


def case(*args: P.args, **kwargs: P.kwargs) -> Case[P]:
    return Case(args=args, kwargs=kwargs)


@dataclasses.dataclass(frozen=True)
class Case(Generic[P]):
    args: tuple
    kwargs: dict
    id: str | None = None
    tags: list[str] | None = None

    def meta(
        self,
        id: str | None = None,
        tags: list[str] | None = None
    ) -> Case[P]:
        if id is not None:
            self = dataclasses.replace(self, id=id)
        if tags:
            self = dataclasses.replace(self, tags=tags)
        return self
