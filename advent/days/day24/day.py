from __future__ import annotations

from typing import Iterator

from .reverse_monad import ReverseMonad

day_num = 24


def part1(lines: Iterator[str]) -> int:
    monad = ReverseMonad.from_str(lines)
    return monad.try_down()


def part2(lines: Iterator[str]) -> int:
    monad = ReverseMonad.from_str(lines)
    return monad.try_up()
