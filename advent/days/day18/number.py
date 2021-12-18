from __future__ import annotations

import abc
import itertools
from typing import Iterator, Literal

from advent.common.char_provider import CharProvider


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
        result = next(numbers)
        for to_add in numbers:
            result = result.add(to_add)
        return result

    @staticmethod
    def find_largest(numbers: Iterator[SnailNumber]) -> int:
        return max(n1.add(n2).magnitude() for n1, n2 in itertools.permutations(numbers, 2))

    @abc.abstractmethod
    def add_int(self, to_add: int, from_left: bool) -> SnailNumber:
        ...

    def single_explode(self) -> SnailNumber:
        if isinstance(self, SnailPair):
            number, _ = self.do_explode(0)
            return number
        else:
            return self

    def single_split(self) -> SnailNumber:
        number, _ = self.do_split()
        return number

    @abc.abstractmethod
    def do_split(self) -> tuple[SnailNumber, bool]:
        ...

    def needs_attention(self) -> Literal["explode", "split"] | None:
        if self.max_level() >= 5:
            return "explode"
        if self.max_digit() >= 10:
            return "split"
        return None

    def max_level(self) -> int:
        return self.get_depths(0)

    @abc.abstractmethod
    def get_depths(self, level: int) -> int:
        ...

    @abc.abstractmethod
    def max_digit(self) -> int:
        ...

    def add(self, other: SnailNumber) -> SnailNumber:
        return SnailPair(self, other).reduce()

    def reduce(self) -> SnailNumber:
        number = self
        attention = number.needs_attention()
        while attention is not None:
            match attention:
                case "explode":
                    number = number.single_explode()
                case "split":
                    number = number.single_split()
            attention = number.needs_attention()
        return number

    @abc.abstractmethod
    def magnitude(self) -> int:
        ...


class SnailInt(SnailNumber):
    @staticmethod
    def create(provider: CharProvider) -> SnailNumber:
        if not provider.peek().isdigit():
            raise Exception()
        number = 0
        while provider.peek().isdigit():
            number = number * 10 + int(provider.get())
        return SnailInt(number)

    def __init__(self, digit: int):
        self.digit = digit

    def __eq__(self, other: object) -> bool:
        if isinstance(other, SnailInt):
            return self.digit == other.digit
        if isinstance(other, SnailPair):
            return False
        raise NotImplementedError

    def add_int(self, to_add: int, from_left: bool) -> SnailNumber:
        return SnailInt(self.digit + to_add)

    def get_depths(self, level: int) -> int:
        return level

    def max_digit(self) -> int:
        return self.digit

    def do_split(self) -> tuple[SnailNumber, bool]:
        if self.digit > 9:
            half = self.digit >> 1
            return SnailPair(SnailInt(half), SnailInt(self.digit - half)), True
        else:
            return self, False

    def __repr__(self) -> str:
        return f"{self.digit}"

    def magnitude(self) -> int:
        return self.digit


class SnailPair(SnailNumber):
    @staticmethod
    def create(provider: CharProvider) -> SnailNumber:
        if provider.get() != "[":
            raise Exception()
        first = SnailNumber.create(provider)
        if provider.get() != ",":
            raise Exception()
        second = SnailNumber.create(provider)
        if provider.get() != "]":
            raise Exception()
        return SnailPair(first, second)

    def __init__(self, first: SnailNumber, second: SnailNumber):
        self.first = first
        self.second = second

    def __eq__(self, other: object) -> bool:
        if isinstance(other, SnailPair):
            return self.first == other.first and self.second == other.second
        if isinstance(other, SnailInt):
            return False
        raise NotImplementedError

    def do_explode(self, level: int) -> tuple[SnailPair, tuple[int | None, int | None] | None]:
        if level < 3:
            if isinstance(self.first, SnailPair):
                first, exploded = self.first.do_explode(level + 1)
                if exploded is not None:
                    add_left, add_right = exploded
                    if add_right is not None:
                        return SnailPair(first, self.second.add_int(
                            add_right, True)), (add_left, None)
                    else:
                        return SnailPair(first, self.second), (add_left, None)
            if isinstance(self.second, SnailPair):
                second, exploded = self.second.do_explode(level + 1)
                if exploded is not None:
                    add_left, add_right = exploded
                    if add_left is not None:
                        return SnailPair(self.first.add_int(add_left, False),
                                         second), (None, add_right)
                    else:
                        return SnailPair(self.first, second), (None, add_right)
            return self, None
        else:
            if isinstance(self.first, SnailPair):
                digits = self.first.get_digits()
                second = self.second.add_int(digits[1], True)
                return SnailPair(SnailInt(0), second), (digits[0], None)
            elif isinstance(self.second, SnailPair):
                digits = self.second.get_digits()
                first = self.first.add_int(digits[0], False)
                return SnailPair(first, SnailInt(0)), (None, digits[1])
            else:
                return self, None

    def get_digits(self) -> tuple[int, int]:
        if isinstance(self.first, SnailInt) and isinstance(self.second, SnailInt):
            return self.first.digit, self.second.digit
        raise Exception()

    def add_int(self, to_add: int, from_left: bool) -> SnailNumber:
        if from_left:
            return SnailPair(self.first.add_int(to_add, True), self.second)
        else:
            return SnailPair(self.first, self.second.add_int(to_add, False))

    def get_depths(self, level: int) -> int:
        return max(self.first.get_depths(level + 1), self.second.get_depths(level + 1))

    def max_digit(self) -> int:
        return max(self.first.max_digit(), self.second.max_digit())

    def do_split(self) -> tuple[SnailNumber, bool]:
        first, finished = self.first.do_split()
        if finished:
            return SnailPair(first, self.second), True
        else:
            second, finished = self.second.do_split()
            if finished:
                return SnailPair(self.first, second), True
        return self, False

    def __repr__(self) -> str:
        return f"[{self.first},{self.second}]"

    def magnitude(self) -> int:
        return 3 * self.first.magnitude() + 2 * self.second.magnitude()
