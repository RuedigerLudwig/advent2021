class Point:
    @staticmethod
    def from_string(point: str) -> "Point":
        parts = point.split(",")
        if len(parts) != 2:
            raise Exception(f"Illegal point {point}")
        x = int(parts[0].strip())
        y = int(parts[1].strip())
        return Point(x, y)

    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    def __eq__(self, other: object) -> bool:
        if type(other) is not Point:
            return False
        return self.x == other.x and self.y == other.y

    def __hash__(self) -> int:
        return hash(self.x) * hash(self.y)

    def __repr__(self) -> str:
        return f"{self.x},{self.y}"

    def __lt__(self, other: "Point") -> bool:
        if self.x == other.x:
            return self.y < other.y
        return self.x < other.x


class Vent:
    @staticmethod
    def from_string(line: str) -> "Vent":
        parts = line.split("->")
        if len(parts) != 2:
            raise Exception(f"Illegal line {line}")
        p1 = Point.from_string(parts[0])
        p2 = Point.from_string(parts[1])

        return Vent(p1, p2)

    def __init__(self, p1: Point, p2: Point) -> None:
        if p1 < p2:
            self.start = p1
            self.end = p2
        else:
            self.start = p2
            self.end = p1

    def __eq__(self, other: object) -> bool:
        if type(other) is not Vent:
            return False
        return self.start == other.start and self.end == other.end

    def __repr__(self) -> str:
        return f"{self.start} -> {self.end}"

    def is_horizontal(self) -> bool:
        return self.start.x == self.end.x

    def is_vertical(self) -> bool:
        return self.start.y == self.end.y

    def all_points(self) -> set[Point]:
        if self.is_horizontal():
            return {Point(self.start.x, p2) for p2 in range(self.start.y, self.end.y + 1)}
        if self.is_vertical():
            return {Point(p1, self.start.y) for p1 in range(self.start.x, self.end.x + 1)}

        steps = self.end.x - self.start.x + 1
        if self.end.y > self.start.y:
            return {Point(self.start.x + s, self.start.y + s) for s in range(steps)}
        else:
            return {Point(self.start.x + s, self.start.y - s) for s in range(steps)}
