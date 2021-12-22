from advent.common import utils
from . import day as Game
from .day import part1, part2


def test_parse():
    input = utils.read_data(21, "test01.txt")
    expected = 4, 8
    result = Game.from_str(input)
    assert result == expected


def test_play_game():
    input = Game.from_str(utils.read_data(21, "test01.txt"))
    expected = 1000, 745, 993
    result = Game.play_game(*input)
    assert result == expected


def test_part1():
    input = utils.read_data(21, "test01.txt")
    expected = 739785
    result = part1(input)
    assert result == expected


def test_part2():
    input = utils.read_data(21, "test01.txt")
    expected = 444356092776315
    result = part2(input)
    assert result == expected
