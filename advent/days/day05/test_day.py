from advent.common import utils

from . import day
from .line import Point, Vent


def test_parse():
    input = "0,9 -> 5,9"
    expected = Vent(Point(0, 9), Point(5, 9))
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
    expected = {Point(2, 1), Point(2, 2)}
    result = input.all_points()
    assert result == expected


def test_intersections():
    input = [Vent.from_string("0,9 -> 5,9"), Vent.from_string("0,9 -> 2,9"), ]
    expected = 3
    result = day.count_intersections(input)
    assert result == expected


def test_part1():
    data = utils.read_data(5, "test01.txt")
    expected = 5
    result = day.part1(data)
    assert result == expected


def test_diagonal():
    input = Vent.from_string("9,7 -> 7,9")
    expected = {Point(9, 7), Point(8, 8), Point(7, 9)}
    result = input.all_points()
    assert result == expected


def test_part2():
    data = utils.read_data(5, "test01.txt")
    expected = 12
    result = day.part2(data)
    assert result == expected
