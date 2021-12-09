from __future__ import annotations

from typing import Callable, Iterator

from advent.common import utils

day_num = 8


def part1(lines: Iterator[str]) -> int:
    return sum(Analyzer.from_str(line).count_easy() for line in lines)


def part2(lines: Iterator[str]) -> int:
    return sum(Analyzer.from_str(line).real_output() for line in lines)


# Since the order of the segment do not matter, I use a set to represent each digit
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
        # The easy digits are defined by their lengths
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

        # Extract all digits with six segmens (6, 9, 0)
        six_segments_bag, bag = utils.split(bag, lambda d: len(d) == 6)

        # 6 is the only six segment digit that does not overlap completely with 1
        six, six_segments_bag = Analyzer.extract_single(six_segments_bag,
                                                        lambda d: not d >= one)

        # Now we can see, which lettter reprsents the upper right segment
        upper_right_segment = one.difference(six)

        # In the bag are only 5 segment digits left (2, 3, 5), they all share the 3
        # horizontal segments
        horiz_segments = eight.intersection(*bag)

        # The 3 is the only digit with 5 segments, that overlaps complete with 1
        three, bag = Analyzer.extract_single(bag, lambda d: d >= one)

        # Now the 2 can be found by getting the only digit left in the bag with an
        # upper right segment
        two, bag = Analyzer.extract_single(
            bag, lambda d: d.issuperset(upper_right_segment))

        # now 5 ist the only digit left in the bag
        five = bag.pop()

        # 9 is the only remaining 6 segment digit, that has all three horizontal segments
        nine, six_segments_bag = Analyzer.extract_single(six_segments_bag,
                                                         lambda d: d >= horiz_segments)

        # finally 0 is the only 6 segment digit left
        zero = six_segments_bag.pop()

        return {zero: 0, one: 1, two: 2, three: 3, four: 4,
                five: 5, six: 6, seven: 7, eight: 8, nine: 9}

    def real_output(self) -> int:
        def value(lst: list[int], pos: int, factor: int, result: int) -> int:
            if pos < 0:
                return result
            return value(lst, pos - 1, factor * 10, result + factor * lst[pos])

        pmap = self.analyze()
        digits = [pmap[digit] for digit in self.output]
        return value(digits, len(digits) - 1, 1, 0)
