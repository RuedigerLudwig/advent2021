from itertools import zip_longest
from typing import Callable, Iterator

Number = list[bool]

day_num = 3


def part1(lines: Iterator[str]) -> int:
    numbers = [convert(line) for line in lines]
    gamma = to_int(calc_gamma(numbers))
    epsilon = to_int(calc_epsilon(numbers))
    return gamma * epsilon


def part2(lines: Iterator[str]) -> int:
    numbers = [convert(line) for line in lines]
    oxygen = to_int(filter_oxygen(numbers))
    co2 = to_int(filter_co2(numbers))
    return oxygen * co2


def convert(line: str) -> Number:
    def _as_bool(c: str) -> bool:
        match c:
            case "0": return False
            case "1": return True
            case _: raise Exception(f"Unknown digit: {c}")

    return [_as_bool(c) for c in line]


def calc_gamma(numbers: list[Number]) -> Number:
    ones: list[int] = []
    for number in numbers:
        ones = [a + (1 if b else -1) for a, b in zip_longest(ones, number, fillvalue=0)]

    return [count >= 0 for count in ones]


def calc_epsilon(numbers: list[Number]) -> Number:
    return [not digit for digit in calc_gamma(numbers)]


def to_int(number: Number) -> int:
    result = 0
    for digit in number:
        result = result << 1 | int(digit)
    return result


def filter(numbers: list[Number], func: Callable[[list[Number]], Number]) -> Number:
    def _filter(numbers: list[Number], pos: int) -> Number:
        crit = func(numbers)[pos]
        next_numbers = [num for num in numbers if num[pos] == crit]
        if len(next_numbers) == 1:
            return next_numbers[0]
        return _filter(next_numbers, pos + 1)

    return _filter(numbers, 0)


def filter_oxygen(numbers: list[list[bool]]) -> Number:
    return filter(numbers, calc_gamma)


def filter_co2(numbers: list[list[bool]]) -> Number:
    return filter(numbers, calc_epsilon)
