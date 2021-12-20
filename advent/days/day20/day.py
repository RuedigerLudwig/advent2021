from __future__ import annotations
from itertools import product

from typing import Iterator


day_num = 20


def part1(lines: Iterator[str]) -> int:
    scanner = Scanner.from_str(lines)
    return len(scanner.process(2).image)


def part2(lines: Iterator[str]) -> int:
    scanner = Scanner.from_str(lines)
    return len(scanner.process(50).image)


Pos = tuple[int, int]


class Scanner:
    @staticmethod
    def from_str(lines: Iterator[str]) -> Scanner:
        algorithm = [pixel == '#' for pixel in next(lines)]
        if len(algorithm) != 512 or (algorithm[0] and algorithm[511]):
            raise Exception("Can't process these kind of images")
        next(lines)
        image = Scanner.read_image(lines)
        return Scanner(algorithm, image, False)

    @staticmethod
    def read_image(lines: Iterator[str]) -> set[Pos]:
        image: set[Pos] = set()
        for y, line in enumerate(lines):
            for x, pixel in enumerate(line):
                if pixel == '#':
                    image.add((x, y))

        return image

    def __init__(self, algorithm: list[bool], image: set[Pos], inverted: bool) -> None:
        self.algorithm = algorithm
        self.image = image
        mnx = min(x for x, _ in self.image) - 1
        mxx = max(x for x, _ in self.image) + 1
        mny = min(y for _, y in self.image) - 1
        mxy = max(y for _, y in self.image) + 1
        self.xrange = (mnx, mxx)
        self.yrange = (mny, mxy)
        self.inverted = inverted

    def do_process(self) -> Scanner:
        do_invert = self.algorithm[0] and not self.inverted
        output: set[Pos] = set()
        for pixel_x in range(self.xrange[0], self.xrange[1] + 1):
            for pixel_y in range(self.yrange[0], self.yrange[1] + 1):
                jump = 0
                for y, x in product([-1, 0, 1], repeat=2):
                    jump *= 2
                    if ((pixel_x + x, pixel_y + y) in self.image) != self.inverted:
                        jump += 1
                if self.algorithm[jump] != do_invert:
                    output.add((pixel_x, pixel_y))
        return Scanner(self.algorithm, output, do_invert)

    def process(self, count: int) -> Scanner:
        scanner = self
        for _ in range(count):
            scanner = scanner.do_process()
        return scanner
