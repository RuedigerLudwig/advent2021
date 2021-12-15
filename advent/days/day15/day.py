from __future__ import annotations

from itertools import count
from queue import PriorityQueue
from typing import Callable, Generator, Iterator

day_num = 15


def part1(lines: Iterator[str]) -> int:
    cave = Cave.from_str(lines)
    return cave.find_path1()


def part2(lines: Iterator[str]) -> int:
    cave = Cave.from_str(lines)
    return cave.find_path2()


Pos = tuple[int, int]
SubPath = tuple[int, Pos]


class Cave:
    @staticmethod
    def from_str(lines: Iterator[str]) -> Cave:
        return Cave([[int(risk) for risk in line] for line in lines])

    def __init__(self, cave: list[list[int]]):
        self.height = len(cave)
        self.width = len(cave[0])
        self.cave: dict[Pos, int] = {}
        for line, y in zip(cave, count()):
            for risk, x in zip(line, count()):
                self.cave[(x, y)] = risk

    def find_path(self, end: Pos, adjacent: Callable[[
                  Cave, Pos], Iterator[tuple[Pos, int]]]) -> int:
        shortest_found: set[Pos] = {(0, 0)}
        queue: PriorityQueue[SubPath] = PriorityQueue()
        queue.put((0, (0, 0)))
        while queue:
            path_risk, pos = queue.get()
            for next_pos, risk in adjacent(self, pos):
                if next_pos not in shortest_found:
                    if next_pos == end:
                        return path_risk + risk
                    shortest_found.add(next_pos)
                    queue.put((path_risk + risk, next_pos))
        raise Exception("No path found")

    deltas: list[Pos] = [(0, -1), (-1, 0), (1, 0), (0, 1)]

    def adjacent(self, pos: Pos) -> Generator[tuple[Pos, int], None, None]:
        for delta in Cave.deltas:
            next_pos = pos[0] + delta[0], pos[1] + delta[1]
            try:
                yield next_pos, self.cave[next_pos]
            except KeyError:
                pass

    def find_path1(self) -> int:
        end = self.width - 1, self.height - 1
        return self.find_path(end, Cave.adjacent)

    def adjacent2(self, pos: Pos) -> Generator[tuple[Pos, int], None, None]:
        for delta in Cave.deltas:
            next_pos = pos[0] + delta[0], pos[1] + delta[1]
            if next_pos[0] >= 0 and next_pos[1] >= 0:
                px, py = next_pos[0] // self.width, next_pos[1] // self.width
                if px < 5 and py < 5:
                    coord = next_pos[0] % self.width, next_pos[1] % self.height
                    yield next_pos, (self.cave[coord] + px + py - 1) % 9 + 1

    def find_path2(self) -> int:
        end = self.width * 5 - 1, self.height * 5 - 1
        return self.find_path(end, Cave.adjacent2)
