from advent.common import utils

from . import day06


def test_parsing():
    input = "3,4,3,1,2"
    expected = [0, 1, 1, 2, 1, 0, 0, 0, 0]
    result = day06.convert(input)
    assert result == expected


def test_day():
    input = [0, 1, 1, 2, 1, 0, 0, 0, 0]
    expected = [1, 1, 2, 1, 0, 0, 0, 0, 0]
    result = day06.age(input)
    assert result == expected


def test_day2():
    input = [0, 1, 1, 2, 1, 0, 0, 0, 0]
    expected = [1, 2, 1, 0, 0, 0, 1, 0, 1]
    result = day06.age(input, 2)
    assert result == expected


def test_day80():
    input = [0, 1, 1, 2, 1, 0, 0, 0, 0]
    expected = 5934
    result = sum(day06.age(input, 80))
    assert result == expected


def test_day256():
    input = [0, 1, 1, 2, 1, 0, 0, 0, 0]
    expected = 26984457539
    result = sum(day06.age(input, 256))
    assert result == expected


def test_part1():
    data = utils.read_data(6, "test01.txt")
    expected = 5934
    result = day06.part1(data)
    assert result == expected


def test_part2():
    data = utils.read_data(6, "test01.txt")
    expected = 26984457539
    result = day06.part2(data)
    assert result == expected
