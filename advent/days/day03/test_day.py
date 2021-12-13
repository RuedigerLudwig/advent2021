from advent.common import utils

from . import day


def test_convert():
    input = "00100"
    expected = [False, False, True, False, False]
    result = day.convert(input)
    assert result == expected


def test_gamma():
    data = [day.convert(line) for line in utils.read_data(3, "test01.txt")]
    expected = [True, False, True, True, False]
    result = day.calc_gamma(data)
    assert result == expected


def test_to_number():
    input = [True, False, True, True, False]
    expected = 22
    result = day.to_int(input)
    assert result == expected


def test_part1():
    data = utils.read_data(3, "test01.txt")
    expected = 198
    result = day.part1(data)
    assert result == expected


def test_oxygen():
    data = [day.convert(line) for line in utils.read_data(3, "test01.txt")]
    expected = [True, False, True, True, True]
    result = day.filter_oxygen(data)
    assert result == expected


def test_co2():
    data = [day.convert(line) for line in utils.read_data(3, "test01.txt")]
    expected = [False, True, False, True, False]
    result = day.filter_co2(data)
    assert result == expected


def test_part2():
    data = utils.read_data(3, "test01.txt")
    expected = 230
    result = day.part2(data)
    assert result == expected
