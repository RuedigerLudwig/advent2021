from __future__ import annotations

from typing import Iterator

day_num = 6


def part1(lines: Iterator[str]) -> int:
    return Swarm.from_str(next(lines)).age(80).size()


def part2(lines: Iterator[str]) -> int:
    return Swarm.from_str(next(lines)).age(256).size()


class Swarm:
    @staticmethod
    def from_str(line: str) -> Swarm:
        ages = [int(num) for num in line.split(",")]
        swarm = [0] * 9
        for age in range(9):
            swarm[age] = sum(1 for f in ages if f == age)
        return Swarm(swarm)

    def __init__(self, swarm: list[int]) -> None:
        self.swarm = swarm

    def age(self, days: int = 1) -> Swarm:
        swarm = self.swarm
        for _ in range(days):
            swarm.append(swarm[0])
            swarm[7] += swarm[0]
            swarm = swarm[1:]
        return Swarm(swarm)

    def size(self) -> int:
        return sum(self.swarm)
