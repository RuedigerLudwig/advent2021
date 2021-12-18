from __future__ import annotations

from typing import Iterator
from .number import SnailNumber

day_num = 18


def part1(lines: Iterator[str]) -> int:
    numbers = (SnailNumber.from_str(line) for line in lines)
    result = SnailNumber.add_all(numbers)
    return result.magnitude()


def part2(lines: Iterator[str]) -> int:
    numbers = (SnailNumber.from_str(line) for line in lines)
    return SnailNumber.find_largest(numbers)
