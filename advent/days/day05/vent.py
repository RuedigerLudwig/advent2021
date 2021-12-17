from __future__ import annotations

Point = tuple[int, int]


class Vent:
    @staticmethod
    def point_from_string(point: str) -> Point:
        match point.split(","):
            case [x, y]:
                return int(x.strip()), int(y.strip())
            case _:
                raise Exception(f"Illegal point {point}")

    @staticmethod
    def from_string(line: str) -> Vent:
        match line.split("->"):
            case [p1, p2]:
                return Vent(Vent.point_from_string(p1), Vent.point_from_string(p2))
            case _:
                raise Exception(f"Illegal line {line}")

    def __init__(self, p1: Point, p2: Point) -> None:
        self.start, self.end = (p1, p2) if p1 < p2 else (p2, p1)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Vent):
            return self.start == other.start and self.end == other.end
        raise NotImplementedError

    def __repr__(self) -> str:
        return f"{self.start} -> {self.end}"

    def is_horizontal(self) -> bool:
        return self.start[0] == self.end[0]

    def is_vertical(self) -> bool:
        return self.start[1] == self.end[1]

    def all_points(self) -> set[Point]:
        if self.is_horizontal():
            return {(self.start[0], p2) for p2 in range(self.start[1], self.end[1] + 1)}
        if self.is_vertical():
            return {(p1, self.start[1]) for p1 in range(self.start[0], self.end[0] + 1)}

        steps = self.end[0] - self.start[0] + 1
        if self.end[1] > self.start[1]:
            return {(self.start[0] + s, self.start[1] + s) for s in range(steps)}
        else:
            return {(self.start[0] + s, self.start[1] - s) for s in range(steps)}
