from __future__ import annotations

import abc
from typing import Any, Generator, Generic, TypeVar, cast

T = TypeVar("T")


class LinkedList(abc.ABC, Generic[T]):
    @staticmethod
    def from_list(lst: list[T]) -> LinkedList[T]:
        if not lst:
            return Nil()
        else:
            return Cont(lst[0], LinkedList.from_list(lst[1:]))

    @staticmethod
    def of(value: T) -> LinkedList[T]:
        return Cont(value, Nil())

    @abc.abstractmethod
    def is_nil(self) -> bool:
        ...

    @abc.abstractmethod
    def head(self) -> T:
        ...

    @abc.abstractmethod
    def tail(self) -> LinkedList[T]:
        ...

    def split(self) -> tuple[T, LinkedList[T]]:
        return self.head(), self.tail()

    def prepend(self, value: T) -> LinkedList[T]:
        return Cont(value, self)

    def __iter__(self) -> Generator[T, None, None]:
        current = self
        while not current.is_nil():
            yield current.head()
            current = current.tail()


class Cont(LinkedList[T]):
    def __init__(self, value: T, next: LinkedList[T]):
        self._value = value
        self._next = next

    def is_nil(self) -> bool:
        return False

    def head(self) -> T:
        return self._value

    def tail(self) -> LinkedList[T]:
        return self._next

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Cont):
            return False
        other = cast(Cont[T], other)
        return self._value == other._value and self._next == other._next

    def __repr__(self) -> str:
        return f"{self._value} -> {self._next}"


class Nil(LinkedList[Any]):
    def is_nil(self) -> bool:
        return True

    def head(self) -> Any:
        raise Exception("No Value in Nil")

    def tail(self) -> LinkedList[Any]:
        raise Exception("No next in Nil")

    def __eq__(self, o: object) -> bool:
        return isinstance(o, Nil)

    def __repr__(self) -> str:
        return "||"
