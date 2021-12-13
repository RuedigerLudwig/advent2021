from typing import Iterator

day_num = 13


def part1(lines: Iterator[str]) -> int:
    paper = Paper.from_str(lines)
    return len(paper.fold_once())


def part2(lines: Iterator[str]) -> list[str]:
    paper = Paper.from_str(lines)
    return Paper.to_str(paper.fold_all())


Point = tuple[int, int]
Fold = tuple[bool, int]


class Paper:
    @staticmethod
    def from_str(lines: Iterator[str]):
        points: set[Point] = set()
        line = next(lines)
        while line:
            points.add(Paper.read_point(line))
            line = next(lines)

        fold = [Paper.read_fold(line) for line in lines]
        return Paper(points, fold)

    @staticmethod
    def read_point(line: str) -> Point:
        match line.split(","):
            case [x, y]:
                return int(x), int(y)
            case _:
                raise Exception(f"Not a valid point '{line}'")

    @staticmethod
    def read_fold(line: str) -> Fold:
        match line.split("="):
            case ["fold along x", val]:
                return True, int(val)
            case ["fold along y", val]:
                return False, int(val)
            case _:
                raise Exception(f"Not a valid fold '{line}'")

    def __init__(self, points: set[Point], folds: list[Fold]) -> None:
        self.points = points
        self.folds = folds

    @staticmethod
    def do_fold(points: set[Point], fold: Fold) -> set[Point]:
        match fold:
            case True, line:
                return {(x if x <= line else 2 * line - x, y)
                        for x, y in points}
            case False, line:
                return {(x, y if y <= line else 2 * line - y)
                        for x, y in points}
            case _:
                raise Exception("Unreachable")

    def fold_once(self) -> set[Point]:
        return Paper.do_fold(self.points, self.folds[0])

    def fold_all(self) -> set[Point]:
        points = self.points
        for fold in self.folds:
            points = Paper.do_fold(points, fold)
        return points

    @staticmethod
    def to_str(points: set[Point]) -> list[str]:
        maxx = max(x for x, _ in points) + 1
        maxy = max(y for _, y in points) + 1

        return ["".join("\u2588" if (x, y) in points else " " for x in range(maxx))
                for y in range(maxy)
                ]
