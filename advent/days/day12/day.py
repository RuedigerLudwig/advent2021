from __future__ import annotations

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

    @staticmethod
    def only_big_twice(cave: str, path: list[str]) -> bool:
        return cave[0].isupper() or cave not in path

    @staticmethod
    def only_big_one_small_twice(cave: str, path: list[str]) -> bool:
        if cave[0].isupper() or cave not in path:
            return True
        if cave == "start":
            return False
        for pos in range(len(path) - 2):
            if path[pos][0].islower() and path[pos] in path[(pos + 1):]:
                return False
        return True

    def extend_path(self, path: list[str], can_visit: Callable[[
                    str, list[str]], bool]) -> list[list[str]]:
        last = path[-1]
        possible = self.system[last]
        result: list[list[str]] = []
        for connection in possible:
            if can_visit(connection, path):
                result.append(path + [connection])
        return result

    def find_all_paths(self, can_visit: Callable[[str, list[str]], bool]) -> int:
        partial: list[list[str]] = [["start"]]
        number_paths = 0
        while partial:
            next_partial: list[list[str]] = []
            for p in partial:
                for path in self.extend_path(p, can_visit):
                    if path[-1] == "end":
                        number_paths += 1
                    else:
                        next_partial.append(path)
            partial = next_partial
        return number_paths

    def all_paths(self) -> int:
        return self.find_all_paths(CaveSystem.only_big_twice)

    def all_paths2(self) -> int:
        return self.find_all_paths(CaveSystem.only_big_one_small_twice)
