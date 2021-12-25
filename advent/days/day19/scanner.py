from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from itertools import combinations, permutations
from typing import Iterator, cast


@dataclass(frozen=True)
class Vector:
    coords: tuple[int, int, int]

    @staticmethod
    def origin() -> Vector:
        return Vector((0, 0, 0))

    @staticmethod
    def from_str(line: str) -> Vector:
        match line.split(","):
            case [x, y, z]:
                return Vector((int(x), int(y), int(z)))
            case _:
                raise Exception(f"Unknonw Pos: {line}")

    @staticmethod
    def from_lst(lst: list[int]) -> Vector:
        match lst:
            case [x, y, z]:
                return Vector((x, y, z))
            case _:
                raise Exception

    def __getitem__(self, pos: int) -> int:
        return self.coords[pos]

    def __add__(self, second: Vector) -> Vector:
        return Vector((self[0] + second[0], self[1] + second[1], self[2] + second[2]))

    def __sub__(self, second: Vector) -> Vector:
        return Vector((self[0] - second[0], self[1] - second[1], self[2] - second[2]))

    def abs(self) -> int:
        return abs(self[0]) + abs(self[1]) + abs(self[2])

    def distance(self, second: Vector) -> int:
        return (self - second).abs()


@dataclass(frozen=True)
class Matrix:
    vectors: tuple[Vector, Vector, Vector]

    @staticmethod
    def from_lst(lst: list[Vector]) -> Matrix:
        match lst:
            case [v1, v2, v3]:
                return Matrix((v1, v2, v3))
            case _:
                raise Exception()

    def __getitem__(self, pos: int) -> Vector:
        return self.vectors[pos]

    def __mul__(self, vec: Vector) -> Vector:
        result = [sum(self[y][x] * vec[x] for x in range(3)) for y in range(3)]
        return Vector.from_lst(result)


class Scanner:
    @staticmethod
    def from_iterator(lines: Iterator[str]) -> list[Scanner]:
        scanners: list[Scanner] = []
        try:
            while True:
                scanners.append(Scanner.from_str(lines))
        except StopIteration:
            return scanners

    @staticmethod
    def from_str(lines: Iterator[str]) -> Scanner:
        next(lines)  # -- scanner ## ---
        beacons: set[Vector] = set()
        for line in lines:
            if not line:
                break
            beacons.add(Vector.from_str(line))
        return Scanner(Scanner.with_fingerprint(beacons), Vector.origin())

    @staticmethod
    def with_fingerprint(beacons: set[Vector]):
        result: dict[Vector, set[int]] = {}
        for a, b in permutations(beacons, 2):
            distance = a.distance(b)
            fingerprint = result.get(a, set())
            fingerprint.add(distance)
            result[a] = fingerprint
        return result

    def __init__(self, beacons: dict[Vector, set[int]], origin: Vector) -> None:
        self.beacons = beacons
        self.origin = origin

    def __repr__(self) -> str:
        return f"{self.beacons}"

    def get_positions(self) -> set[Vector]:
        return cast(set[Vector], self.beacons.keys())

    def transpose(self, matrix: Matrix) -> Scanner:
        new_beacons = {(matrix * pos): finger for pos, finger in self.beacons.items()}
        new_origin = matrix * self.origin
        return Scanner(new_beacons, new_origin)

    def move(self, vec: Vector) -> Scanner:
        new_beacons = {(f + vec): n for f, n in self.beacons.items()}
        new_origin = self.origin + vec
        return Scanner(new_beacons, new_origin)

    @staticmethod
    def determine_matrix(lst: tuple[tuple[Vector, Vector], tuple[Vector, Vector]]) -> Matrix:
        def sign(num: int) -> int:
            return 1 if num >= 0 else -1

        d01 = lst[0][0] - lst[1][0]
        d11 = lst[0][1] - lst[1][1]

        matrix: list[Vector] = []

        for dim in range(3):
            if abs(d11[0]) == abs(d01[dim]):
                matrix.append(Vector((sign(d11[0]) // sign(d01[dim]), 0, 0)))
            elif abs(d11[1]) == abs(d01[dim]):
                matrix.append(Vector((0, sign(d11[1]) // sign(d01[dim]), 0)))
            else:
                matrix.append(Vector((0, 0, sign(d11[2]) // sign(d01[dim]))))

        return Matrix.from_lst(matrix)

    def get_transpose_func(self, other: Scanner):
        first: tuple[Vector, Vector] | None = None
        for fst_beacon, fst_fingerprint in self.beacons.items():
            for snd_beacon, snd_fingerprint in other.beacons.items():
                identical = snd_fingerprint.intersection(fst_fingerprint)
                if len(identical) >= 11:
                    if first is None:
                        first = fst_beacon, snd_beacon
                    else:
                        matrix = Scanner.determine_matrix((first, (fst_beacon, snd_beacon)))
                        snd_turned = (matrix * snd_beacon)
                        new_origin = fst_beacon - snd_turned
                        return new_origin, matrix
        return None

    @staticmethod
    def match_all(lst: list[Scanner]) -> deque[Scanner]:
        def do_match(matched_lst: deque[Scanner], unmatched: Scanner) -> Scanner | None:
            for matched in matched_lst:
                result = matched.get_transpose_func(unmatched)
                if result is not None:
                    move, matrix = result
                    return unmatched.transpose(matrix).move(move)
            return None

        matched_lst: deque[Scanner] = deque()
        matched_lst.append(lst[0])
        unmatched_lst = deque(lst[1:])
        last_matched = 0
        while unmatched_lst:
            to_match = unmatched_lst.popleft()
            now_matched = do_match(matched_lst, to_match)
            if now_matched is not None:
                matched_lst.append(now_matched)
                last_matched = 0
            else:
                last_matched += 1
                if last_matched > len(unmatched_lst):
                    raise Exception("Cannot find further match")
                unmatched_lst.append(to_match)

        return matched_lst

    @staticmethod
    def merge_all(lst: list[Scanner]) -> set[Vector]:
        matched = Scanner.match_all(lst)
        empty: set[Vector] = set()
        return empty.union(*[s.get_positions() for s in matched])

    @staticmethod
    def max_distance(lst: list[Scanner]) -> int:
        matched = Scanner.match_all(lst)
        return max(o1.origin.distance(o2.origin) for o1, o2 in combinations(matched, 2))
