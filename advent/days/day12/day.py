from __future__ import annotations
from itertools import islice

from typing import Callable, Iterator

day_num = 12


def part1(lines: Iterator[str]) -> int:
    system = CaveSystem.from_str(lines)
    return system.all_paths()


def part2(lines: Iterator[str]) -> int:
    system = CaveSystem.from_str(lines)
    return system.all_paths2()


class CaveSystem:
    @staticmethod
    def get_connection(line: str) -> tuple[str, str]:
        match line.split("-"):
            case [p1, p2]:
                return p1, p2
            case _:
                raise Exception(f"Too many connections {line}")

    @staticmethod
    def build_system(possible: set[tuple[str, str]], current: str, result: dict[str, set[str]]):
        exits: set[str] = set()
        for connection in possible:
            if connection[0] == current:
                exits.add(connection[1])
            elif connection[1] == current:
                exits.add(connection[0])

        result[current] = exits
        for exit in exits:
            if exit not in result.keys():
                CaveSystem.build_system(possible, exit, result)

    @staticmethod
    def from_str(lines: Iterator[str]) -> CaveSystem:
        connections = {CaveSystem.get_connection(line) for line in lines}
        result: dict[str, set[str]] = {}
        CaveSystem.build_system(connections, "start", result)
        return CaveSystem(result)

    def __init__(self, system: dict[str, set[str]]) -> None:
        self.system = system

    def extend_path(self, path: list[str], can_visit: Callable[[
                    str, list[str]], bool]) -> list[list[str]]:
        return [path + [connection]
                for connection in self.system[path[-1]]
                if can_visit(connection, path)]

    def find_all_paths(self, can_visit: Callable[[str, list[str]], bool]) -> int:
        def _find_all_paths(prev: list[str]) -> int:
            number_paths = 0

            for path in self.extend_path(prev, can_visit):
                if path[-1] == "end":
                    number_paths += 1
                else:
                    number_paths += _find_all_paths(path)
            return number_paths
        return _find_all_paths(["start"])

    def all_paths(self) -> int:
        def only_big_twice(cave: str, path: list[str]) -> bool:
            return cave[0].isupper() or cave not in path

        return self.find_all_paths(only_big_twice)

    def all_paths2(self) -> int:
        def only_big_one_small_twice(cave: str, path: list[str]) -> bool:
            if cave[0].isupper() or cave not in path:
                return True
            if cave == "start":
                return False
            for pos in range(1, len(path) - 2):
                if path[pos][0].islower() and path[pos] in islice(path, pos + 1, None):
                    return False
            return True
        return self.find_all_paths(only_big_one_small_twice)
