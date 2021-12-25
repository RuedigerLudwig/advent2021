from __future__ import annotations

from typing import Iterator

day_num = 25


def part1(lines: Iterator[str]) -> int:
    marina = MarinaBottom.from_str(lines)
    return marina.step()


def part2(lines: Iterator[str]) -> None:
    pass


class MarinaBottom:
    @staticmethod
    def from_str(lines: Iterator[str]) -> MarinaBottom:
        bottom: list[list[bool | None]] = []
        for line in lines:
            row: list[bool | None] = []
            for cell in line:
                match cell:
                    case '>':
                        row.append(True)
                    case 'v':
                        row.append(False)
                    case _:
                        row.append(None)
            bottom.append(row)

        return MarinaBottom(bottom)

    def __init__(self, bottom: list[list[bool | None]]) -> None:
        self.bottom = bottom
        self.width = len(bottom[0])
        self.height = len(bottom)

    def step(self):
        steps = 0
        next_bottom = self.bottom
        moved = True
        while moved:
            moved = False
            east_bottom = [row.copy() for row in next_bottom]
            for y in range(self.height):
                for x in range(self.width):
                    if next_bottom[y][x] is True:
                        next_x = (x + 1) % self.width
                        if next_bottom[y][next_x] is None:
                            east_bottom[y][next_x] = True
                            east_bottom[y][x] = None
                            moved = True
            next_bottom = [row.copy() for row in east_bottom]
            for x in range(self.width):
                for y in range(self.height):
                    if east_bottom[y][x] is False:
                        next_y = (y + 1) % self.height
                        if east_bottom[next_y][x] is None:
                            next_bottom[next_y][x] = False
                            next_bottom[y][x] = None
                            moved = True
            steps += 1
        return steps
