import typing

ResultType = int | list[str]


@typing.runtime_checkable
class Day(typing.Protocol):
    day_num: int

    @staticmethod
    def part1(lines: typing.Iterator[str]) -> ResultType | None:
        ...

    @staticmethod
    def part2(lines: typing.Iterator[str]) -> ResultType | None:
        ...
