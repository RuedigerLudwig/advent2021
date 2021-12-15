from __future__ import annotations

import sys
from queue import PriorityQueue
from typing import Callable, Iterator

day_num = 15


def part1(lines: Iterator[str]) -> int:
    cave = Cave.from_str(lines)
    return cave.find_path1()


def part2(lines: Iterator[str]) -> int:
    cave = Cave.from_str(lines)
    return cave.find_path2()


# x, y
Pos = tuple[int, int]
# value, last Position
SubPath = tuple[int, Pos]


class Cave:
    @staticmethod
    def from_str(lines: Iterator[str]) -> Cave:
        return Cave([[int(risk) for risk in line] for line in lines])

    def __init__(self, cave: list[list[int]]):
        self.height = len(cave)
        self.width = len(cave[0])
        self.cave = cave

    def find_path(self, start: Pos, end: Pos,
                  adjacent: Callable[[Pos], Iterator[tuple[Pos, int]]]) -> int:
        shortest_path: dict[Pos, int] = {start: 0}
        queue: PriorityQueue[SubPath] = PriorityQueue()
        queue.put((0, start))
        while queue:
            path_risk, pos = queue.get()
            if pos == end:
                return path_risk

            for next_pos, risk in adjacent(pos):
                next_risk = path_risk + risk
                if shortest_path.get(next_pos, sys.maxsize) > next_risk:
                    shortest_path[next_pos] = next_risk
                    queue.put((next_risk, next_pos))
        raise Exception("No path found")

    deltas: list[Pos] = [(0, -1), (-1, 0), (1, 0), (0, 1)]

    def find_path1(self) -> int:
        def _adjacent(pos: Pos) -> Iterator[tuple[Pos, int]]:
            for delta in Cave.deltas:
                nx, ny = pos[0] + delta[0], pos[1] + delta[1]
                if nx >= 0 and ny >= 0 and nx < self.width and ny < self.height:
                    yield (nx, ny), self.cave[ny][nx]

        end = self.width - 1, self.height - 1
        return self.find_path((0, 0), end, _adjacent)

    def find_path2(self) -> int:
        def _adjacent(pos: Pos) -> Iterator[tuple[Pos, int]]:
            for delta in Cave.deltas:
                nx, ny = pos[0] + delta[0], pos[1] + delta[1]
                if nx >= 0 and ny >= 0:
                    px, py = nx // self.width, ny // self.width
                    if px < 5 and py < 5:
                        ox, oy = nx % self.width, ny % self.height
                        yield (nx, ny), (self.cave[oy][ox] + px + py - 1) % 9 + 1

        end = self.width * 5 - 1, self.height * 5 - 1
        return self.find_path((0, 0), end, _adjacent)
