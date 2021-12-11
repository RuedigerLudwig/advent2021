from __future__ import annotations

from itertools import count, product
from typing import Iterator

day_num = 11


def part1(lines: Iterator[str]) -> int:
    octopy = Octopy.from_str(lines)
    return octopy.count_flashes_after_steps(100)


def part2(lines: Iterator[str]) -> int:
    octopy = Octopy.from_str(lines)
    return octopy.count_steps_to_sync()


State = tuple[int, bool]


class Octopy:
    @staticmethod
    def from_str(lines: Iterator[str]) -> Octopy:
        return Octopy([[(int(octopus), False) for octopus in line] for line in lines])

    def __init__(self, octopy: list[list[State]]):
        self.height = len(octopy)
        self.width = len(octopy[0])
        assert all(len(line) == self.width for line in octopy)
        self.octopy: list[list[State]] = octopy

    def flash(self, x: int, y: int):
        self.octopy[y][x] = 0, True
        for ny, nx in product(range(max(y - 1, 0), min(y + 2, self.height)),
                              range(max(x - 1, 0), min(x + 2, self.width))):
            match self.octopy[ny][nx]:
                case level, False:
                    self.octopy[ny][nx] = level + 1, False

    def step(self) -> int:
        flashes = 0
        self.octopy = [[(level + 1, False) for level, _ in line] for line in self.octopy]

        x, y = 0, 0
        while y < len(self.octopy):
            match self.octopy[y][x]:
                case level, False if level > 9:
                    self.flash(x, y)
                    flashes += 1
                    x, y = max(x - 1, 0), max(y - 1, 0)
                case _:
                    x += 1
                    if x >= len(self.octopy[y]):
                        x, y = 0, y + 1
        return flashes

    def count_flashes_after_steps(self, steps: int) -> int:
        return sum(self.step() for _ in range(steps))

    def count_steps_to_sync(self) -> int:
        for step in count(1):
            flashes = self.step()
            if flashes == self.width * self.height:
                return step
        raise Exception("Unreachable")
