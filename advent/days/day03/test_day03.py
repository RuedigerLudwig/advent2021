from advent.common import utils

from . import day03


def test_day03():
    pass


def test_convert():
    input = "00100"
    expected = [False, False, True, False, False]
    result = day03.convert(input)
    assert result == expected


def test_count():
    input = [[False, False, True, False, False],
             [True, True, True, True, False],
             [True, False, True, True, False]]
    expected = [2, 1, 3, 2, 0]
    result = day03.count(input)
    assert result == expected


def test_gamma():
    data = [day03.convert(line) for line in utils.read_data(3, "test01.txt")]
    expected = [True, False, True, True, False]
    result = day03.calc_gamma(data)
    assert result == expected


def test_inverse():
    input = [True, False, True, True, False]
    expected = [False, True, False, False, True]
    result = day03.invers(input)
    assert result == expected


def test_to_number():
    input = [True, False, True, True, False]
    expected = 22
    result = day03.to_number(input)
    assert result == expected


def test_part1():
    data = utils.read_data(3, "test01.txt")
    expected = 198
    result = day03.part1(data)
    assert result == expected


def test_oxygen():
    data = [day03.convert(line) for line in utils.read_data(3, "test01.txt")]
    expected = [True, False, True, True, True]
    result = day03.filter_oxygen(data)
    assert result == expected


def test_co2():
    data = [day03.convert(line) for line in utils.read_data(3, "test01.txt")]
    expected = [False, True, False, True, False]
    result = day03.filter_co2(data)
    assert result == expected


def test_part2():
    data = utils.read_data(3, "test01.txt")
    expected = 230
    result = day03.part2(data)
    assert result == expected
