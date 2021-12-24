from __future__ import annotations

import sys
from dataclasses import dataclass, field
from itertools import chain, islice, tee
from queue import PriorityQueue
from typing import Iterator

day_num = 23


def part1(lines: Iterator[str]) -> int:
    result = AmphipodHome.from_str(lines)
    return result.find_path()


def part2(orig: Iterator[str]) -> int:
    front, end = tee(orig, 2)
    lines = chain(islice(front, 3), [
        "  #D#C#B#A#",
        "  #D#B#A#C#"
    ], islice(end, 3, None))
    result = AmphipodHome.from_str(lines)
    return result.find_path()


Location = tuple[int, int]

H1: Location = 4, 0
H2: Location = 4, 1
H3: Location = 4, 2
H4: Location = 4, 3
H5: Location = 4, 4
H6: Location = 4, 5
H7: Location = 4, 6
X1: Location = -1, 0
X2: Location = -1, 1
X3: Location = -1, 2
X4: Location = -1, 3
A1: Location = 0, 0
B1: Location = 1, 0
C1: Location = 2, 0
D1: Location = 3, 0
A2: Location = 0, 1
B2: Location = 1, 1
C2: Location = 2, 1
D2: Location = 3, 1

A = 0
B = 1
C = 2
D = 3

neighborhood: dict[Location, list[Location]] = {
    H1: [H2],
    H2: [H1, X1],
    X1: [H2, H3, A1],
    H3: [X1, X2],
    X2: [H3, H4, B1],
    H4: [X2, X3],
    X3: [H4, H5, C1],
    H5: [X3, X4],
    X4: [H5, H6, D1],
    H6: [X4, H7],
    H7: [H6],
    A1: [X1],
    B1: [X2],
    C1: [X3],
    D1: [X4],
}


@dataclass(order=True)
class PrioTurtles:
    cost: int
    state: AmphipodHome = field(compare=False)


class AmphipodHome:
    @staticmethod
    def from_str(lines: Iterator[str]) -> AmphipodHome:
        next(lines)
        next(lines)
        a: list[int | None] = []
        b: list[int | None] = []
        c: list[int | None] = []
        d: list[int | None] = []

        occupants = "ABCD"

        finished = False
        while not finished:
            match next(lines)[3:10].split("#"):
                case [a1, b1, c1, d1]:
                    a.append(occupants.index(a1))
                    b.append(occupants.index(b1))
                    c.append(occupants.index(c1))
                    d.append(occupants.index(d1))
                case _:
                    finished = True

        hallway: list[int | None] = [None] * 7

        return AmphipodHome([a, b, c, d, hallway])

    def __init__(self, layout: list[list[int | None]]):
        self._layout = layout

        self._bits: int | None = None

    @property
    def max_pos(self) -> int:
        return len(self._layout[0])

    @property
    def bits(self) -> int:
        def add_bits(bits: int, lst: list[int | None]) -> int:
            for item in lst:
                if item is None:
                    bits = (bits << 3) | 0x07
                else:
                    bits = (bits << 3) | item
            return bits

        if self._bits is None:
            bits = add_bits(0, self._layout[0])
            bits = add_bits(bits, self._layout[1])
            bits = add_bits(bits, self._layout[2])
            bits = add_bits(bits, self._layout[3])
            bits = add_bits(bits, self._layout[4])
            self._bits = bits
        return self._bits

    def __eq__(self, other: object) -> bool:
        if isinstance(other, AmphipodHome):
            return self.bits == other.bits
        raise NotImplementedError

    def __hash__(self) -> int:
        return hash(self.bits)

    def __iter__(self) -> Iterator[tuple[Location, int]]:
        for wing, row in enumerate(self._layout):
            for pos, occupant in enumerate(row):
                if occupant is not None:
                    yield (wing, pos), occupant

    def print(self) -> None:
        def item(row: int, pos: int) -> str:
            result = self[(row, pos)]
            if result is None:
                return "."
            else:
                return "ABCD"[result]

        print("#############")
        print(
            "#{}{}.{}.{}.{}.{}{}#".format(
                item(4, 0), item(4, 1),
                item(4, 2), item(4, 3),
                item(4, 4), item(4, 5),
                item(4, 6)))
        print("###{}#{}#{}#{}###".format(item(0, 0), item(1, 0), item(2, 0), item(3, 0)))
        for row in range(1, self.max_pos):
            print("  #{}#{}#{}#{}#".format(item(0, row), item(1, row), item(2, row), item(3, row)))
        print("  #########")

    def __getitem__(self, room: Location) -> int | None:
        if room[0] < 0 or room[0] > 4:
            return None
        return self._layout[room[0]][room[1]]

    def move(self, from_room: Location, to_room: Location) -> AmphipodHome:
        occupant = self._layout[from_room[0]][from_room[1]]
        if occupant is None or self._layout[to_room[0]][to_room[1]] is not None:
            raise Exception

        new_layout = [wing.copy() for wing in self._layout]
        new_layout[from_room[0]][from_room[1]] = None
        new_layout[to_room[0]][to_room[1]] = occupant

        return AmphipodHome(new_layout)

    @staticmethod
    def is_hallway(room: Location) -> bool:
        return room[0] == 4

    @staticmethod
    def is_sideroom(room: Location) -> bool:
        return room[0] >= 0 and room[0] < 4

    def is_bottom_sideroom(self, loc: Location) -> bool:
        return loc[0] >= 0 and loc[0] < 4 and loc[1] == len(self._layout[loc[0]]) - 1

    @staticmethod
    def is_home(room: Location, occupant: int) -> bool:
        return room[0] == occupant

    def enter_home_at_pos(self, check_occupant: int) -> int | None:
        wing = self._layout[check_occupant]
        for occupant in wing:
            if occupant is not None and occupant != check_occupant:
                return None
        for pos, occupant in enumerate(wing):
            if occupant is not None:
                if pos > 0:
                    return pos - 1
                else:
                    return None
        return len(wing) - 1

    def wing_finished(self, row: int) -> bool:
        for occupant in self._layout[row]:
            if occupant != row:
                return False
        return True

    def all_wings_finished(self) -> bool:
        return all(self.wing_finished(row) for row in [A, B, C, D])

    def find_home(self, occupant: int, path: list[Location]) -> tuple[Location, int] | None:
        for room in neighborhood[path[-1]]:
            if room in path:
                continue
            if AmphipodHome.is_home(room, occupant):
                pos = self.enter_home_at_pos(occupant)
                if pos is not None:
                    return (occupant, pos), len(path) + pos
            if not AmphipodHome.is_sideroom(room):
                if self[room] is None:
                    result = self.find_home(occupant, path + [room])
                    if result is not None:
                        return result
        return None

    def steps_to_leave(self, room: Location) -> list[Location] | None:
        for pos in range(room[1] - 1, -1, -1):
            if self._layout[room[0]][pos] is not None:
                return None
        return [(room[0], pos) for pos in range(room[1], -1, -1)]

    def ampipod_finished(self, room: Location) -> bool:
        return (AmphipodHome.is_sideroom(room)
                and all(occupant == room[0] for occupant in self._layout[room[0]][room[1]:]))

    def find_hallways(self, room: Location) -> Iterator[list[Location]]:
        def all_paths(path: list[Location]) -> Iterator[list[Location]]:
            for neighbor in neighborhood[path[-1]]:
                if neighbor not in path and not AmphipodHome.is_sideroom(neighbor):
                    if self[neighbor] is None:
                        newpath = path + [neighbor]
                        if AmphipodHome.is_hallway(neighbor):
                            yield newpath
                        yield from all_paths(newpath)

        if AmphipodHome.is_sideroom(room):
            steps = self.steps_to_leave(room)
            if steps is not None:
                yield from all_paths(steps)
        else:
            yield from all_paths([room])

    @staticmethod
    def weighted(occupant: int, moves: int) -> int:
        return moves * 10 ** occupant

    def possible_paths_for(self, start: Location, occupant: int) -> Iterator[tuple[Location, int]]:
        if not AmphipodHome.is_hallway(start) and not self.ampipod_finished(start):
            for path in self.find_hallways(start):
                yield path[-1], AmphipodHome.weighted(occupant, len(path) - 1)

    def apply_finish_moves(self) -> tuple[AmphipodHome, int]:
        for room, occupant in self:
            if AmphipodHome.is_hallway(room):
                result = self.find_home(occupant, [room])
                if result is not None:
                    next_state = self.move(room, result[0])
                    exit_state, cost = next_state.apply_finish_moves()
                    return exit_state, cost + self.weighted(occupant, result[1])
        return self, 0

    def possible_paths(self) -> Iterator[tuple[AmphipodHome, int]]:
        next_state, finish_costs = self.apply_finish_moves()
        if finish_costs > 0:
            yield next_state, finish_costs
        else:
            for room, occupant in self:
                for next_room, move_cost in self.possible_paths_for(room, occupant):
                    next_state = self.move(room, next_room)
                    yield next_state, move_cost

    def find_path(self):
        found: dict[AmphipodHome, int] = {self: 0}
        queue: PriorityQueue[PrioTurtles] = PriorityQueue()
        queue.put(PrioTurtles(0, self))
        while queue:
            current = queue.get()
            if current.state.all_wings_finished():
                return current.cost

            for next_state, move_cost in current.state.possible_paths():
                next_cost = move_cost + current.cost
                old_cost = found.get(next_state, sys.maxsize)
                if old_cost > next_cost:
                    found[next_state] = next_cost
                    queue.put(PrioTurtles(next_cost, next_state))

        raise Exception
