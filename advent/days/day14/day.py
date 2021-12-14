from __future__ import annotations

from collections import Counter
from itertools import pairwise
from typing import Iterator

day_num = 14


def part1(lines: Iterator[str]) -> int:
    poly = Polymer.from_str(lines)
    return poly.cook_polymer(10).minmax()


def part2(lines: Iterator[str]) -> int:
    poly = Polymer.from_str(lines)
    return poly.cook_polymer(40).minmax()


Pair = tuple[str, str]


class Polymer:
    @staticmethod
    def from_str(lines: Iterator[str]) -> Polymer:
        line = next(lines)
        start = line[0]
        template = dict(Counter(pairwise(line)))
        next(lines)

        rules = dict(Polymer.read_rule(line) for line in lines)
        return Polymer(template, rules, start)

    @staticmethod
    def read_rule(line: str) -> tuple[Pair, str]:
        match line.strip().split("->"):
            case [f, to]:
                pair = f[0], f[1]
                return pair, to.strip()
            case _:
                raise Exception

    def __init__(self, polymer: dict[Pair, int], rules: dict[Pair, str], start: str):
        self.polymer = polymer
        self.rules = rules
        self.start = start

    def cook_polymer(self, count: int) -> Polymer:
        polymer = self.polymer
        for _ in range(count):
            next_polymer: dict[Pair, int] = {}
            for key, count in polymer.items():
                inserted = self.rules[key]
                next_polymer[key[0], inserted] = next_polymer.get((key[0], inserted), 0) + count
                next_polymer[inserted, key[1]] = next_polymer.get((inserted, key[1]), 0) + count
            polymer = next_polymer
        return Polymer(polymer, self.rules, self.start)

    def minmax(self) -> int:
        counter: dict[str, int] = {self.start: 1}
        for (_, b), count in self.polymer.items():
            counter[b] = counter.get(b, 0) + count

        return max(counter.values()) - min(counter.values())
