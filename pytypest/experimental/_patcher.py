from __future__ import annotations

from typing import Any, Generic, Iterator, MutableMapping, TypeVar

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
        if name.startswith('_AttrPatcher__'):
            return super().__setattr__(name, value)
        if isinstance(self.__target, str):
            self.__target
            self.__patcher.setattr(f'{self.__target}.{name}', value)
        else:
            self.__patcher.setattr(self.__target, name, value)

    def __delattr__(self, name: str) -> None:
        if name.startswith('_AttrPatcher__'):
            return super().__delattr__(name)
        self.__patcher.delattr(self.__target, name)


class ItemPatcher(Generic[K, V]):
    def __init__(
        self,
        patcher: pytest.MonkeyPatch,
        target: MutableMapping[K, V],
    ) -> None:
        self._patcher = patcher
        self._target = target
        self._used: bool = False

    def __setitem__(self, name: K, value: V) -> None:
        self._patcher.setitem(self._target, name, value)
        self._used = True

    def __delitem__(self, name: K) -> None:
        self._patcher.delitem(self._target, name)
        self._used = True


@fixture
def patcher(target: object | str) -> Iterator[Any]:
    monkey_patcher = pytest.MonkeyPatch()
    yield AttrPatcher(monkey_patcher, target)
    monkey_patcher.undo()


@fixture
def item_patcher(target: MutableMapping[K, V]) -> Iterator[ItemPatcher[K, V]]:
    monkey_patcher = pytest.MonkeyPatch()
    item_patcher = ItemPatcher(monkey_patcher, target)
    yield item_patcher
    monkey_patcher.undo()
    if not item_patcher._used:
        raise RuntimeError('item_patcher is instantiated but not used')
