from advent.common import utils

from . import day
from .aim import Aim
from .command import Command
from .pos import Pos


def test_translate_forward():
    input = "forward 8"
    expected = Command(8, 0)
    result = Command.from_str(input)
    assert result == expected


def test_translate_up():
    input = "up 10"
    expected = Command(0, -10)
    result = Command.from_str(input)
    assert result == expected


def test_translate_down():
    input = "down 1"
    expected = Command(0, 1)
    result = Command.from_str(input)
    assert result == expected


def test_pos_adding():
    pos = Pos(1, 0)
    cmd = Command(0, 7)
    expected = Pos(1, 7)
    result = pos.move(cmd)
    assert result == expected


def test_part1():
    data = utils.read_data(2, "test01.txt")
    expected = 150
    result = day.part1(data)
    assert result == expected


def test_aim_add():
    aim = Aim(5, 5, 0)
    cmd = Command(8, 0)
    expected = Aim(13, 5, 40)
    result = aim.move(cmd)
    assert result == expected


def test_aim_add2():
    aim = Aim(13, 5, 40)
    cmd = Command(0, -3)
    expected = Aim(13, 2, 40)
    result = aim.move(cmd)
    assert result == expected


def test_part2():
    data = utils.read_data(2, "test01.txt")
    expected = 900
    result = day.part2(data)
    assert result == expected
