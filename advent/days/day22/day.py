from __future__ import annotations

from itertools import combinations
from typing import Iterator

day_num = 22


def part1(lines: Iterator[str]) -> int:
    cubes = [Command.from_str(line, number) for number, line in enumerate(lines)]
    return Command.merge_small(cubes)


def part2(lines: Iterator[str]) -> int:
    cubes = [Command.from_str(line, number) for number, line in enumerate(lines)]
    return Command.merge_big(cubes)


Range = tuple[int, int]
Pos = tuple[int, int, int]


class Cube:
    @staticmethod
    def from_str(line: str) -> Cube:
        match line.split(","):
            case [x, y, z]:
                return Cube(Cube.get_range(x), Cube.get_range(y), Cube.get_range(z))
            case _:
                raise Exception

    @staticmethod
    def get_range(line: str) -> Range:
        match(line.split("=")):
            case [_, range]:
                match range.split(".."):
                    case [start, end]:
                        return int(start), int(end)
        raise Exception

    def __init__(self, x_range: Range, y_range: Range, z_range: Range):
        self.x_range = x_range
        self.y_range = y_range
        self.z_range = z_range

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Cube):
            return (self.x_range == other.x_range
                    and self.y_range == other.y_range
                    and self.z_range == other.z_range)
        raise NotImplementedError

    def __repr__(self) -> str:
        s = self.size()
        x = f"x={self.x_range[0]}..{self.x_range[1]}"
        y = f"y={self.y_range[0]}..{self.y_range[1]}"
        z = f"z={self.z_range[0]}..{self.z_range[1]}"
        return f"{s}: {x},{y},{z}"

    def size(self) -> int:
        return ((self.x_range[1] - self.x_range[0] + 1)
                * (self.y_range[1] - self.y_range[0] + 1)
                * (self.z_range[1] - self.z_range[0] + 1))

    def get_cubes(self) -> set[Pos]:
        return {(x, y, z)
                for x in range(self.x_range[0], self.x_range[1] + 1)
                for y in range(self.y_range[0], self.y_range[1] + 1)
                for z in range(self.z_range[0], self.z_range[1] + 1)
                }

    def contains(self, other: Cube) -> bool:
        return (self.x_range[0] <= other.x_range[0]
                and self.x_range[1] >= other.x_range[1]
                and self.y_range[0] <= other.y_range[0]
                and self.y_range[1] >= other.y_range[1]
                and self.z_range[0] <= other.z_range[0]
                and self.z_range[1] >= other.z_range[1]
                )

    @ staticmethod
    def overlap(first: Range, second: Range) -> Range | None:
        start = max(first[0], second[0])
        end = min(first[1], second[1])
        if start <= end:
            return start, end
        else:
            return None

    def intersection(self, other: Cube) -> Cube | None:
        x_over = Cube.overlap(self.x_range, other.x_range)
        y_over = Cube.overlap(self.y_range, other.y_range)
        z_over = Cube.overlap(self.z_range, other.z_range)
        if x_over is None or y_over is None or z_over is None:
            return None
        return Cube(x_over, y_over, z_over)

    @staticmethod
    def all_intersections(cubes: Iterator[Cube]) -> Cube | None:
        if not cubes:
            return None
        result = next(cubes)
        for cube in cubes:
            result = result.intersection(cube)
            if result is None:
                return None
        return result


class Command:
    @staticmethod
    def from_str(line: str, number: int) -> Command:
        match line.split():
            case ['on', rest]:
                cube = Cube.from_str(rest)
                return Command(number, True, cube)
            case ['off', rest]:
                cube = Cube.from_str(rest)
                return Command(number, False, cube)
            case _:
                raise Exception

    def __init__(self, number: int, on: bool, cube: Cube):
        self.number = number
        self.on = on
        self.cube = cube
        self.excludes: list[Cube] = []

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Command):
            return (self.number == other.number and self.on == other.on
                    and self.cube == other.cube)
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.number}: {self.on} -> {self.cube.size()} - {len(self.excludes)}"

    def add_exclude(self, exclude: Cube) -> None:
        self.excludes.append(exclude)

    def merge_into(self, cubes: Iterator[Pos]) -> Iterator[Pos]:
        my_cubes = self.cube.get_cubes()
        for cube in cubes:
            if cube not in my_cubes:
                yield cube
        if self.on:
            for cube in my_cubes:
                yield cube

    def is_small(self) -> bool:
        return self.cube.x_range[0] >= -50 and self.cube.x_range[0] <= 50

    @staticmethod
    def merge_small(cubes: list[Command]) -> int:
        result: Iterator[Pos] = iter([])
        for cube in cubes:
            if cube.is_small():
                result = cube.merge_into(result)
        return sum(1 for _ in result)

    def size(self) -> int:
        def get_exclude_size(num: int) -> int:
            result = 0
            for x in combinations(self.excludes, num):
                intersect = Cube.all_intersections(iter(x))
                if intersect is not None:
                    result += intersect.size()
            return result

        if self.excludes:
            result = self.cube.size()
            add = -1
            for num in range(1, len(self.excludes) + 1):
                result += add * get_exclude_size(num)
                add *= -1

            return result
        else:
            return self.cube.size()

    @staticmethod
    def merge_big(cubes: list[Command]) -> int:
        to_do = list(reversed(cubes))
        result = 0
        while to_do:
            current = to_do[0]
            to_do = to_do[1:]
            for command in to_do:
                intersect = current.cube.intersection(command.cube)
                if intersect is not None:
                    command.add_exclude(intersect)
            if current.on:
                result += current.size()

        return result
