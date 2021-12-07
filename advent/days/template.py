import typing

ResultType = int


class Day(typing.Protocol):
    day_num: int

    @staticmethod
    def part1(lines: list[str]) -> ResultType | None:
        ...

    @staticmethod
    def part2(lines: list[str]) -> ResultType | None:
        ...
