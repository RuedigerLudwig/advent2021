from functools import reduce
from itertools import zip_longest
from typing import Callable, Iterator, cast

Number = list[bool]

day_num = 3


def part1(lines: Iterator[str]) -> int:
    numbers = [convert(line) for line in lines]
    gamma_list = calc_gamma(numbers)
    gamma = to_int(gamma_list)
    epsilon = to_int(invers(gamma_list))
    return gamma * epsilon


def part2(lines: Iterator[str]) -> int:
    numbers = [convert(line) for line in lines]
    oxygen = to_int(filter_oxygen(numbers))
    co2 = to_int(filter_co2(numbers))
    return oxygen * co2


def convert(line: str) -> Number:
    def as_bool(c: str) -> bool:
        match c:
            case "0": return False
            case "1": return True
            case _: raise Exception(f"Unknown digit: {c}")

    return [as_bool(c) for c in line]


def count_ones(numbers: list[Number]) -> list[int]:
    def add_number(prev: list[int], number: Number) -> list[int]:
        return [a + int(b) for a, b in zip_longest(prev, number, fillvalue=0)]

    return reduce(add_number, numbers, cast(list[int], []))


def calc_gamma(numbers: list[Number]) -> Number:
    ones = count_ones(numbers)
    expected_ones = len(numbers) / 2
    return [c >= expected_ones for c in ones]


def calc_epsilon(numbers: list[Number]) -> Number:
    return invers(calc_gamma(numbers))


def invers(number: Number) -> Number:
    return [not n for n in number]


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
