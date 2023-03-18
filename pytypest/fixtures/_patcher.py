from __future__ import annotations

from typing import Generic, Iterator, MutableMapping, TypeVar

import pytest

from .._fixture_factory import fixture

K = TypeVar('K')
V = TypeVar('V')


class AttrPatcher:
    def __init__(
        self,
        patcher: pytest.MonkeyPatch,
        target: object | str,
    ) -> None:
        self.__patcher = patcher
        self.__target = target

    def __setattr__(self, name: str, value: object) -> None:
        if isinstance(self.__target, str):
            self.__target
            self.__patcher.setattr(f'{self.__target}.{name}', value)
        else:
            self.__patcher.setattr(self.__target, name, value)

    def __delattr__(self, name: str) -> None:
        self.__patcher.delattr(self.__target, name)


class ItemPatcher(Generic[K, V]):
    def __init__(
        self,
        patcher: pytest.MonkeyPatch,
        target: MutableMapping[K, V],
    ) -> None:
        self.__patcher = patcher
        self.__target = target

    def __setitem__(self, name: K, value: V) -> None:
        self.__patcher.setitem(self.__target, name, value)

    def __delitem__(self, name: K) -> None:
        self.__patcher.delitem(self.__target, name)


@fixture
def patcher(target: object | str) -> Iterator[AttrPatcher]:
    monkey_patcher = pytest.MonkeyPatch()
    yield AttrPatcher(monkey_patcher, target)
    monkey_patcher.undo()


@fixture
def item_patcher(target: MutableMapping[K, V]) -> Iterator[ItemPatcher[K, V]]:
    monkey_patcher = pytest.MonkeyPatch()
    yield ItemPatcher(monkey_patcher, target)
    monkey_patcher.undo()
