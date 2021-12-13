from advent.common import utils

from . import day


def test_convert():
    input = ["1", "2", "3"]
    expected = [1, 2, 3]
    result = list(day.convert(iter(input)))
    assert result == expected


def test_part1():
    data = utils.read_data(1, "test01.txt")
    expected = 7
    result = day.part1(data)
    assert result == expected


def test_part2():
    data = utils.read_data(1, "test01.txt")
    expected = 5
    result = day.part2(data)
    assert result == expected
