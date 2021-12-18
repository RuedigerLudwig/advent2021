from __future__ import annotations

import abc
import itertools
from functools import reduce
from typing import Iterator

from advent.common.char_provider import CharProvider
from advent.common.char_reader import CharReader


class SnailNumber(abc.ABC):
    @staticmethod
    def from_str(line: str) -> SnailNumber:
        return SnailNumber.create(CharProvider(line))

    @staticmethod
    def create(provider: CharProvider) -> SnailNumber:
        if provider.peek() == "[":
            return SnailPair.create(provider)
        return SnailInt.create(provider)

    @staticmethod
    def add_all(numbers: Iterator[SnailNumber]) -> SnailNumber:
        return reduce(lambda a, b: a + b, numbers)

    @staticmethod
    def find_largest(numbers: Iterator[SnailNumber]) -> int:
        return max((n1 + n2).magnitude() for n1, n2 in itertools.permutations(numbers, 2))

    @abc.abstractmethod
    def add_int(self, to_add: int, from_left: bool) -> SnailNumber:
        ...

    @abc.abstractmethod
    def explode(self, level: int) -> tuple[SnailNumber, tuple[int | None, int | None] | None]:
        ...

    @abc.abstractmethod
    def split(self) -> tuple[SnailNumber, bool]:
        ...

    @abc.abstractmethod
    def magnitude(self) -> int:
        ...

    @abc.abstractmethod
    def get_value(self) -> int:
        ...

    def __add__(self, other: SnailNumber) -> SnailNumber:
        number = SnailPair(self, other)
        finished = False
        while not finished:
            explode = True
            while explode:
                number, done = number.explode(0)
                explode = done is not None
            number, did_split = number.split()
            finished = not did_split
        return number


class SnailInt(SnailNumber):
    @staticmethod
    def create(provider: CharProvider) -> SnailNumber:
        return SnailInt(CharReader.read_unsigned_int(provider))

    def __init__(self, value: int):
        self._value = value

    def __eq__(self, other: object) -> bool:
        if isinstance(other, SnailInt):
            return self._value == other._value
        if isinstance(other, SnailNumber):
            return False
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self._value}"

    def get_value(self) -> int:
        return self._value

    def add_int(self, to_add: int, from_left: bool) -> SnailNumber:
        return SnailInt(self._value + to_add)

    def explode(self, level: int) -> tuple[SnailNumber, tuple[int | None, int | None] | None]:
        return self, None

    def split(self) -> tuple[SnailNumber, bool]:
        if self._value > 9:
            half = self._value >> 1
            return SnailPair(SnailInt(half), SnailInt(self._value - half)), True
        else:
            return self, False

    def magnitude(self) -> int:
        return self._value


class SnailPair(SnailNumber):
    @staticmethod
    def create(provider: CharProvider) -> SnailNumber:
        CharReader.read_word(provider, "[")
        first = SnailNumber.create(provider)
        CharReader.read_word(provider, ",")
        second = SnailNumber.create(provider)
        CharReader.read_word(provider, "]")

        return SnailPair(first, second)

    def __init__(self, first: SnailNumber, second: SnailNumber):
        self.first = first
        self.second = second

    def __eq__(self, other: object) -> bool:
        if isinstance(other, SnailPair):
            return self.first == other.first and self.second == other.second
        if isinstance(other, SnailNumber):
            return False
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"[{self.first},{self.second}]"

    def get_value(self) -> int:
        raise Exception("No Value in a SnailPair")

    def explode(self, level: int) -> tuple[SnailNumber, tuple[int | None, int | None] | None]:
        if level < 4:
            first, exploded = self.first.explode(level + 1)
            if exploded is not None:
                add_left, add_right = exploded
                if add_right is not None:
                    return SnailPair(first, self.second.add_int(
                        add_right, True)), (add_left, None)
                else:
                    return SnailPair(first, self.second), (add_left, None)

            second, exploded = self.second.explode(level + 1)
            if exploded is not None:
                add_left, add_right = exploded
                if add_left is not None:
                    return SnailPair(self.first.add_int(add_left, False),
                                     second), (None, add_right)
                else:
                    return SnailPair(self.first, second), (None, add_right)

            return self, None
        else:
            return SnailInt(0), (self.first.get_value(), self.second.get_value())

    def add_int(self, to_add: int, from_left: bool) -> SnailNumber:
        if from_left:
            return SnailPair(self.first.add_int(to_add, True), self.second)
        else:
            return SnailPair(self.first, self.second.add_int(to_add, False))

    def split(self) -> tuple[SnailNumber, bool]:
        first, finished = self.first.split()
        if finished:
            return SnailPair(first, self.second), True
        else:
            second, finished = self.second.split()
            if finished:
                return SnailPair(self.first, second), True
        return self, False

    def magnitude(self) -> int:
        return 3 * self.first.magnitude() + 2 * self.second.magnitude()
