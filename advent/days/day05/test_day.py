from advent.common import utils

from . import day
from .vent import Vent


def test_parse():
    input = "0,9 -> 5,9"
    expected = Vent((0, 9), (5, 9))
    result = Vent.from_string(input)
    assert result == expected


def test_vertical():
    input = "0,9 -> 5,9"
    expected = True
    result = Vent.from_string(input).is_vertical()
    assert result == expected


def test_horizontal():
    input = "2,2 -> 2,1"
    expected = True
    result = Vent.from_string(input).is_horizontal()
    assert result == expected


def test_straight_points():
    input = Vent.from_string("2,2 -> 2,1")
    expected = {(2, 1), (2, 2)}
    result = input.all_points()
    assert result == expected


def test_intersections():
    input = [Vent.from_string("0,9 -> 5,9"), Vent.from_string("0,9 -> 2,9")]
    expected = 3
    result = day.count_intersections(iter(input))
    assert result == expected


def test_part1():
    data = utils.read_data(5, "test01.txt")
    expected = 5
    result = day.part1(data)
    assert result == expected


def test_diagonal():
    input = Vent.from_string("9,7 -> 7,9")
    expected = {(9, 7), (8, 8), (7, 9)}
    result = input.all_points()
    assert result == expected


def test_part2():
    data = utils.read_data(5, "test01.txt")
    expected = 12
    result = day.part2(data)
    assert result == expected
