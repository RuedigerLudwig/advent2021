from typing import Callable


def part1(lines: list[str]) -> int:
    return Crab.from_str(lines[0]).min_propcost()


def part2(lines: list[str]) -> int:
    return Crab.from_str(lines[0]).min_geocost()


class Crab():
    @staticmethod
    def from_str(line: str) -> "Crab":
        crabs = [int(num) for num in line.split(",")]
        return Crab(crabs)

    def __init__(self, crabs: list[int]):
        self.crabs = crabs

    def find_least_cost(self, start_pos: int, cost_fun: Callable[[list[int], int], int]) -> int:
        def approach(pos: int, last: int, step: int) -> int:
            next_pos = pos + step
            cost = cost_fun(self.crabs, next_pos)
            if cost > last:
                return last
            return approach(next_pos, cost, step)

        cost0 = cost_fun(self.crabs, start_pos)
        cost1 = cost_fun(self.crabs, start_pos + 1)
        if cost0 > cost1:
            return approach(start_pos + 1, cost1, 1)
        else:
            return approach(start_pos, cost0, -1)

    def median(self) -> int:
        s = sorted(self.crabs)
        return s[len(s) >> 1]

    @staticmethod
    def calc_propcost(crabs: list[int], pos: int) -> int:
        return sum(abs(p - pos) for p in crabs)

    def min_propcost(self) -> int:
        return self.find_least_cost(self.median(), Crab.calc_propcost)

    def average(self) -> int:
        return int(sum(self.crabs) / len(self.crabs))

    @staticmethod
    def calc_geocost(crabs: list[int], pos: int) -> int:
        def gauss(n: int) -> int:
            return (n * (n + 1)) >> 1

        return sum(gauss(abs(p - pos)) for p in crabs)

    def min_geocost(self) -> int:
        return self.find_least_cost(self.average(), Crab.calc_geocost)
