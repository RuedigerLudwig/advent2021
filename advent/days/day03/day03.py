from functools import reduce
from itertools import zip_longest
from typing import Callable

Number = list[bool]


def part1(lines: list[str]) -> int:
    numbers = [convert(line) for line in lines]
    gamma_list = calc_gamma(numbers)
    gamma = to_number(gamma_list)
    epsilon = to_number(invers(gamma_list))
    return gamma * epsilon


def part2(lines: list[str]) -> int:
    numbers = [convert(line) for line in lines]
    oxygen = to_number(filter_oxygen(numbers))
    co2 = to_number(filter_co2(numbers))
    return oxygen * co2


def convert(line: str) -> Number:
    def digit(c: str) -> bool:
        match c:
            case "0": return False
            case "1": return True
            case _: raise Exception(f"Unknown digit: '{c}'")

    return [digit(c) for c in line.strip()]


def count(numbers: list[Number]) -> list[int]:
    def add(lst: list[int], ab: tuple[int, bool]) -> list[int]:
        a, b = ab
        return lst + [a + int(b)]

    def add_number(prev: list[int], number: Number) -> list[int]:
        combined = zip_longest(prev, number, fillvalue=0)
        return reduce(add, combined, [])

    return reduce(add_number, numbers, [])


def calc_gamma(numbers: list[Number]) -> Number:
    ones = count(numbers)
    mean_val = len(numbers) / 2
    return [c >= mean_val for c in ones]


def invers(number: Number) -> Number:
    return [not n for n in number]


def to_number(number: Number) -> int:
    def _to_num(pos: int, result: int, fact: int) -> int:
        if pos < 0:
            return result
        new_result = result + fact if number[pos] else result
        return _to_num(pos - 1, new_result, fact * 2)
    return _to_num(len(number) - 1, 0, 1)


def filter(numbers: list[Number], func: Callable[[list[Number]], Number]) -> Number:
    for pos in range(len(numbers[0])):
        crit = func(numbers)[pos]
        numbers = [num for num in numbers if num[pos] == crit]
        if len(numbers) == 1:
            return numbers[0]

    raise Exception("Did not find a solitair Number")


def filter_oxygen(numbers: list[list[bool]]) -> list[bool]:
    return filter(numbers, calc_gamma)


def filter_co2(numbers: list[list[bool]]) -> list[bool]:
    return filter(numbers, lambda n: invers(calc_gamma(n)))
