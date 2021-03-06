from __future__ import annotations

from itertools import product
from typing import Iterator

day_num = 17


def part1(lines: Iterator[str]) -> int:
    probe = Target.from_str(next(lines))
    mx = max(y for _, y in probe.get_possible())
    return mx * (mx + 1) >> 1


def part2(lines: Iterator[str]) -> int:
    probe = Target.from_str(next(lines))
    return probe.count_possible()


Range = tuple[int, int]
XStepRange = tuple[int, int | None]
YStepRange = tuple[int, int]
Pos = tuple[int, int]


class Target:
    @staticmethod
    def from_str(line: str) -> Target:
        def get_range(text: str) -> Range:
            match text.split(".."):
                case [start, end]:
                    return int(start.strip()), int(end.strip())
                case _:
                    raise NotImplementedError

        match line.split(","):
            case [x, y]:
                range_x = get_range(x.split("=")[1])
                range_y = get_range(y.split("=")[1])
                return Target(range_x, range_y)
            case _:
                raise NotImplementedError

    def __init__(self, range_x: Range, range_y: Range) -> None:
        self.range_x = range_x
        self.range_y = range_y

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Target):
            return self.range_x == other.range_x and self.range_y == other.range_y
        raise NotImplementedError

    def possible_x(self) -> Iterator[tuple[int, XStepRange]]:
        for x_start in range(1, self.range_x[1] + 1):
            min_steps: int | None = None
            steps = 1
            x_pos = x_start
            x_vel = x_start - 1
            done = False
            while not done:
                if x_pos > self.range_x[1]:
                    if min_steps is not None:
                        yield x_start, (min_steps, steps - 1)
                    done = True

                elif x_pos >= self.range_x[0] and min_steps is None:
                    min_steps = steps

                elif x_vel == 0:
                    if min_steps is not None:
                        yield x_start, (min_steps, None)
                    done = True

                steps += 1
                x_pos += x_vel
                x_vel -= 1

    def possible_y(self) -> Iterator[tuple[int, YStepRange]]:
        for y_start in range(self.range_y[0], -self.range_y[0] + 1):
            if y_start <= 0:
                steps = 1
                y_vel = y_start - 1
            else:
                steps = y_start * 2 + 2
                y_vel = -y_start - 2
            min_steps = None
            y_pos = y_vel + 1
            done = False
            while not done:
                if y_pos < self.range_y[0]:
                    if min_steps is not None:
                        yield y_start, (min_steps, steps - 1)
                    done = True
                elif y_pos <= self.range_y[1] and min_steps is None:
                    min_steps = steps

                steps += 1
                y_pos += y_vel
                y_vel -= 1

    def get_possible(self) -> Iterator[Pos]:
        posx = self.possible_x()
        posy = self.possible_y()
        for (x, (min_x, max_x)), (y, (min_y, max_y)) in product(posx, posy):
            mn = max(min_x, min_y)
            mx = max_y if max_x is None else min(max_x, max_y)
            if mn <= mx:
                yield x, y

    def count_possible(self) -> int:
        return sum(1 for _ in self.get_possible())
