from __future__ import annotations

import sys
from dataclasses import dataclass, field
from functools import cached_property, reduce
from itertools import chain, islice, tee
from queue import PriorityQueue
from typing import Iterator

day_num = 23


def part1(lines: Iterator[str]) -> int:
    result = Layout.from_str(lines)
    return result.find_path()


def part2(orig: Iterator[str]) -> int:
    front, end = tee(orig, 2)
    lines = chain(islice(front, 3), [
        "  #D#C#B#A#",
        "  #D#B#A#C#"
    ], islice(end, 3, None))
    result = Layout.from_str(lines)
    return result.find_path()


class Amphipod(int):
    @staticmethod
    def from_str(char: str) -> Amphipod:
        return Amphipod("ABCD".find(char))

    def __str__(self) -> str:
        return "ABCD"[self]

    @property
    def weight(self) -> int:
        return 10 ** self

    @staticmethod
    def all() -> Iterator[Amphipod]:
        for value in range(4):
            yield Amphipod(value)


class Hallway(int):
    @property
    def wing(self) -> Amphipod:
        return Amphipod(4)

    @property
    def pos(self) -> int:
        return self

    def path_to_wing(self, wing: Amphipod) -> Iterator[tuple[Location, int]]:
        if self < wing + 2:
            for pos in range(self + 1, wing + 2):
                yield Hallway(pos), 1 if pos == 1 else 2
        else:
            for pos in range(self - 1, wing + 1, -1):
                yield Hallway(pos), 1 if pos == 5 else 2
        yield Wing((wing, 0)), 2


class Wing(tuple[Amphipod, int]):
    @property
    def wing(self) -> Amphipod:
        return self[0]

    @property
    def pos(self) -> int:
        return self[1]

    def is_home(self, occupant: Amphipod | None) -> bool:
        return occupant is not None and self[0] == occupant

    def path_to_wing(self, wing: Amphipod) -> Iterator[tuple[Location, int]]:
        if self[0] != wing:
            if self[0] < wing:
                for num in range(self[0] + 2, wing + 2):
                    yield Hallway(num), 2
            else:
                for num in range(self[0] + 1, wing + 1, -1):
                    yield Hallway(num), 2
            yield Wing((wing, 0)), 2

    def path_to_hallway(self, hallway: Hallway) -> Iterator[tuple[Location, int]]:
        if self[0] + 1 > hallway.pos:
            for pos in range(self[0] + 1, hallway.pos - 1, -1):
                yield Hallway(pos), 1 if pos == 0 else 2
        else:
            for pos in range(self[0] + 2, hallway.pos + 1):
                yield Hallway(pos), 1 if pos == 6 else 2


Location = Hallway | Wing


@dataclass(order=True)
class PrioTuple:
    cost: int
    layout: Layout = field(compare=False)


class Layout:
    @staticmethod
    def from_str(lines: Iterator[str]) -> Layout:
        next(lines)  # north wall
        next(lines)  # hallway

        wing_a: list[Amphipod | None] = []
        wing_b: list[Amphipod | None] = []
        wing_c: list[Amphipod | None] = []
        wing_d: list[Amphipod | None] = []

        finished = False
        while not finished:
            match next(lines)[3:10].split("#"):
                case [a, b, c, d]:
                    wing_a.append(Amphipod.from_str(a))
                    wing_b.append(Amphipod.from_str(b))
                    wing_c.append(Amphipod.from_str(c))
                    wing_d.append(Amphipod.from_str(d))
                case _:  # south wall
                    finished = True

        hallway: list[Amphipod | None] = [None] * 7
        return Layout([wing_a, wing_b, wing_c, wing_d, hallway])

    def __init__(self, layout: list[list[Amphipod | None]]):
        self._layout = layout

    def get(self, room: Location) -> Amphipod | None:
        if isinstance(room, Hallway):
            return self._layout[4][room]
        else:
            return self._layout[room.wing][room.pos]

    def all_moveable(self) -> Iterator[tuple[Location, Amphipod]]:
        yield from self.all_in_hallways()
        yield from self.all_moveable_in_wings()

    def all_moveable_in_wings(self) -> Iterator[tuple[Wing, Amphipod]]:
        for wing in Amphipod.all():
            for depth, occupant in enumerate(self._layout[wing]):
                if occupant is not None:
                    yield Wing((wing, depth)), occupant
                    break

    def all_in_hallways(self) -> Iterator[tuple[Hallway, Amphipod]]:
        for pos, occupant in enumerate(self._layout[4]):
            if occupant is not None:
                yield Hallway(pos), occupant

    def all_in_wing(self, wing: Amphipod) -> Iterator[tuple[Wing, Amphipod | None]]:
        for depth, occupant in enumerate(self._layout[wing]):
            yield Wing((wing, depth)), occupant

    @cached_property
    def bits(self) -> int:
        def add_bits(bits: int, rooms: list[Amphipod | None]) -> int:
            for occupant in rooms:
                if occupant is None:
                    bits = (bits << 3) | 0x07
                else:
                    bits = (bits << 3) | occupant
            return bits

        return reduce(add_bits, self._layout, 0)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, Layout):
            return self.bits == other.bits
        raise NotImplementedError

    def __hash__(self) -> int:
        return hash(self.bits)

    def __str__(self) -> str:
        def item(occupant: Amphipod | None) -> str:
            return "." if occupant is None else str(occupant)

        result = "#############\n#"
        for pos, occupant in enumerate(self._layout[4]):
            result += item(occupant)
            if pos not in [0, 5, 6]:
                result += " "
        result += "#\n"

        first = True
        for (_, a), (_, b), (_, c), (_, d) in zip(self.all_in_wing(Amphipod(0)),
                                                  self.all_in_wing(Amphipod(1)),
                                                  self.all_in_wing(Amphipod(2)),
                                                  self.all_in_wing(Amphipod(3))):
            result += "##" if first else "  "
            result += f"#{item(a)}#{item(b)}#{item(c)}#{item(d)}#"
            result += "##\n" if first else "  \n"
            first = False
        result += "  #########"

        return result

    def move(self, from_room: Location, to_room: Location) -> Layout:
        new_layout = [rooms.copy() for rooms in self._layout]
        occupant = self.get(from_room)
        new_layout[from_room.wing][from_room.pos] = None
        new_layout[to_room.wing][to_room.pos] = occupant

        return Layout(new_layout)

    def wing_finished(self, wing: Amphipod) -> bool:
        return all(room.is_home(occupant) for room, occupant in self.all_in_wing(wing))

    def all_wings_finished(self) -> bool:
        return all(self.wing_finished(wing) for wing in Amphipod.all())

    # Only enter if there are only correct occupants
    def may_enter_homewing_at(self, amphipod: Amphipod) -> Wing | None:
        last_empty: Wing | None = None
        for room, occupant in self.all_in_wing(amphipod):
            if occupant is None:
                last_empty = room
            elif not room.is_home(occupant):
                return None
        return last_empty

    def has_wrong_occupants(self, wing: Amphipod) -> bool:
        return any(occupant is not None and not room.is_home(occupant)
                   for room, occupant in self.all_in_wing(wing))

    def steps_to_home(self, from_room: Location, to_wing: Amphipod) -> int | None:
        path_steps = 0
        for room, steps in from_room.path_to_wing(to_wing):
            if self.get(room) is not None:
                return None
            path_steps += steps
        return path_steps

    def apply_finish_moves(self) -> tuple[Layout, int]:
        for room, occupant in self.all_moveable():
            final_room: Wing | None = None
            start_steps = 0

            if isinstance(room, Hallway):
                final_room = self.may_enter_homewing_at(occupant)
            elif not room.is_home(occupant):
                final_room = self.may_enter_homewing_at(occupant)
                start_steps = room.pos

            if final_room is None:
                continue

            if (path_steps := self.steps_to_home(room, occupant)) is not None:
                next_layout = self.move(room, final_room)
                cost = occupant.weight * (start_steps + path_steps + final_room.pos)
                final, finish_cost = next_layout.apply_finish_moves()
                return final, cost + finish_cost
        return self, 0

    def walk_into_hallway(self, from_room: Wing, to_room: Hallway,
                          occupant: Amphipod) -> Iterator[tuple[Layout, int]]:
        path_steps = from_room.pos
        for hallway, steps in from_room.path_to_hallway(to_room):
            if self.get(hallway) is None:
                next_layout = self.move(from_room, hallway)
                path_steps += steps
                cost = occupant.weight * path_steps
                next_layout, finish_cost = next_layout.apply_finish_moves()
                yield next_layout, cost + finish_cost
            else:
                return

    def possible_paths(self) -> Iterator[tuple[Layout, int]]:
        for room, occupant in self.all_moveable_in_wings():
            if self.has_wrong_occupants(room.wing):
                yield from self.walk_into_hallway(room, Hallway(0), occupant)
                yield from self.walk_into_hallway(room, Hallway(6), occupant)

    def find_path(self):
        found: dict[Layout, int] = {self: 0}
        queue: PriorityQueue[PrioTuple] = PriorityQueue()
        queue.put(PrioTuple(0, self))
        while not queue.empty():
            current = queue.get()
            if current.layout.all_wings_finished():
                return current.cost

            for next_layout, path_cost in current.layout.possible_paths():
                next_cost = path_cost + current.cost
                old_cost = found.get(next_layout, sys.maxsize)
                if old_cost > next_cost:
                    found[next_layout] = next_cost
                    queue.put(PrioTuple(next_cost, next_layout))

        raise Exception
