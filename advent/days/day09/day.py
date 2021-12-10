from __future__ import annotations

from itertools import count
from math import prod
from typing import Generator, Iterator

day_num = 9


def part1(lines: Iterator[str]) -> int:
    cave = Cave.from_str(lines)
    return cave.get_cave_risklevel()


def part2(lines: Iterator[str]) -> int:
    cave = Cave.from_str(lines)
    all_basin = cave.get_sorted_basin_sizes()
    return prod(all_basin[:3])


Location = tuple[int, int]


def add(fst: Location, snd: Location) -> Location:
    return fst[0] + snd[0], fst[1] + snd[1]


class Cave:
    deltas: list[Location] = [(0, -1), (-1, 0), (1, 0), (0, 1)]

    @staticmethod
    def from_str(lines: Iterator[str]) -> Cave:
        raw = ((int(p) for p in line) for line in lines)

        # Remove all locations of height 9, that way we can later treat these and
        # the cave walls the same
        heightmap = {(x, y): height for line, y in zip(raw, count())
                     for height, x in zip(line, count()) if height < 9}

        return Cave(heightmap)

    def __init__(self, heightmap: dict[Location, int]):
        self.heightmap = heightmap

    def adjacent(self, location: Location) -> Generator[tuple[Location, int], None, None]:
        for delta in Cave.deltas:
            next_location = add(location, delta)
            try:
                yield next_location, self.heightmap[next_location]
            except KeyError:
                pass

    def find_lowpoints(self) -> set[Location]:
        return {location
                for location, height in self.heightmap.items()
                if height < min(h for _, h in self.adjacent(location))}

    def get_cave_risklevel(self) -> int:
        return sum(self.heightmap[location] + 1 for location in self.find_lowpoints())

    def get_basin_size(self, start: Location) -> int:
        visited: set[Location] = set()

        def walk_to(location: Location):
            visited.add(location)
            for next_location, _ in self.adjacent(location):
                if next_location not in visited:
                    walk_to(next_location)

        walk_to(start)
        return len(visited)

    def get_sorted_basin_sizes(self) -> list[int]:
        return sorted((self.get_basin_size(lowpoint)
                      for lowpoint in self.find_lowpoints()), reverse=True)
