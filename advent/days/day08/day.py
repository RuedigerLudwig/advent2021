from __future__ import annotations

from typing import Callable, Iterator

from advent.common import utils

day_num = 8


def part1(lines: Iterator[str]) -> int:
    return sum(Analyzer.from_str(line).count_easy() for line in lines)


def part2(lines: Iterator[str]) -> int:
    return sum(Analyzer.from_str(line).real_output() for line in lines)


Digit = frozenset[str]


class Analyzer:
    @staticmethod
    def from_str(line: str) -> Analyzer:
        parts = line.split("|")
        if len(parts) != 2:
            raise Exception("Need exactly two parts")
        pattern = parts[0].split()
        if len(pattern) != 10:
            raise Exception("Unknown pattern")
        output = parts[1].split()
        return Analyzer(pattern, output)

    @staticmethod
    def extract_single(bag: set[Digit], pred: Callable[[Digit], bool]) -> tuple[Digit, set[Digit]]:
        item, new_bag = utils.split(bag, pred)
        return item.pop(), new_bag

    def __init__(self, pattern: list[str], output: list[str]):
        self.pattern = {Digit(p) for p in pattern}
        self.output = [Digit(o) for o in output]

    def get_easy(self) -> tuple[list[Digit], set[Digit]]:
        one, bag = Analyzer.extract_single(self.pattern, lambda d: len(d) == 2)
        four, bag = Analyzer.extract_single(bag, lambda d: len(d) == 4)
        seven, bag = Analyzer.extract_single(bag, lambda d: len(d) == 3)
        eight, bag = Analyzer.extract_single(bag, lambda d: len(d) == 7)
        return [one, four, seven, eight], bag

    def count_easy(self) -> int:
        easy, _ = self.get_easy()
        return sum(1 for digit in self.output if digit in easy)

    def analyze(self) -> dict[Digit, int]:
        [one, four, seven, eight], bag = self.get_easy()

        six_bars_bag, bag = utils.split(bag, lambda d: len(d) == 6)
        six, six_bars_bag = Analyzer.extract_single(six_bars_bag,
                                                    lambda d: not d.issuperset(one))

        upper_right_bar = one.difference(six)
        horiz_bars = eight.intersection(*bag)

        three, bag = Analyzer.extract_single(bag, lambda d: d.issuperset(one))
        two, bag = Analyzer.extract_single(bag, lambda d: d.issuperset(upper_right_bar))
        five = bag.pop()

        nine, six_bars_bag = Analyzer.extract_single(six_bars_bag,
                                                     lambda d: d.issuperset(horiz_bars))
        zero = six_bars_bag.pop()

        return {zero: 0, one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8, nine: 9}

    def real_output(self) -> int:
        def value(lst: list[int], pos: int, factor: int, result: int) -> int:
            if pos < 0:
                return result
            return value(lst, pos - 1, factor * 10, result + factor * lst[pos])

        pmap = self.analyze()
        digits = [pmap[digit] for digit in self.output]
        return value(digits, len(digits) - 1, 1, 0)
