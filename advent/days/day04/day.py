from typing import Iterator
from .game import Game

day_num = 4


def part1(lines: Iterator[str]) -> int:
    game = Game.from_str(lines)
    result = game.play_game()
    if result is None:
        raise Exception("No winner found")
    return result[0] * result[1].get_num_value()


def part2(lines: Iterator[str]) -> int:
    game = Game.from_str(lines)
    result = game.play_for_last()
    if result is None:
        raise Exception("No last winner found")
    return result[0] * result[1].get_num_value()
