from .line import Vent, Point


def part1(lines: list[str]) -> int:
    vents = [Vent.from_string(line) for line in lines]
    return count_intersections([v for v in vents if v.is_horizontal() or v.is_vertical()])


def part2(lines: list[str]) -> int:
    vents = [Vent.from_string(line) for line in lines]
    return count_intersections(vents)


def count_intersections(lines: list[Vent]) -> int:
    all_points: set[Point] = set()
    intersect_points: set[Point] = set()
    for line in lines:
        points = line.all_points()
        intersect_points |= (all_points & points)
        all_points |= points
    return len(intersect_points)
