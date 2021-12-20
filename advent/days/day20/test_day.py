from advent.common import utils
from .day import Scanner, part1, part2


def test_parse():
    input = utils.read_data(20, "test01.txt")
    expected = 512
    result = len(Scanner.from_str(input).algorithm)
    assert result == expected


def test_process():
    input = Scanner.from_str(utils.read_data(20, "test01.txt"))
    expected = 35
    result = len(input.process(2).image)
    assert result == expected


def test_part1():
    input = utils.read_data(20, "test01.txt")
    expected = 35
    result = part1(input)
    assert result == expected


def test_part2():
    input = utils.read_data(20, "test01.txt")
    expected = 3351
    result = part2(input)
    assert result == expected
