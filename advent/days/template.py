import typing


class Day(typing.Protocol):
    @staticmethod
    def part1(lines: list[str]) -> int | None:
        ...

    @staticmethod
    def part2(lines: list[str]) -> int | None:
        ...
