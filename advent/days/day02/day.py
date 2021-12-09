from functools import reduce
from typing import Iterable, Iterator

from .aim import Aim
from .command import Command
from .pos import Pos

day_num = 2


def part1(lines: Iterator[str]) -> int:
    end_pos = reduce(Pos.move, convert(lines), Pos(0, 0))
    return end_pos.horiz * end_pos.depth


def part2(lines: Iterator[str]) -> int:
    end_pos = reduce(Aim.move, convert(lines), Aim(0, 0, 0))
    return end_pos.horiz * end_pos.depth


def convert(lines: Iterator[str]) -> Iterable[Command]:
    return (Command.from_str(line) for line in lines)
