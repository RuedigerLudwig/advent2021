from functools import reduce
from typing import Iterable

from advent.common import utils

from .aim import Aim
from .command import Command
from .pos import Pos

day_num = 2


def part1(lines: list[str]) -> int:
    end_pos = reduce(Pos.move, convert(lines), Pos(0, 0))
    return end_pos.horiz * end_pos.depth


def part2(lines: list[str]) -> int:
    end_pos = reduce(Aim.move, convert(lines), Aim(0, 0, 0))
    return end_pos.horiz * end_pos.depth


def convert(lines: list[str]) -> Iterable[Command]:
    return utils.some_filter(Command.from_str(line) for line in lines)
