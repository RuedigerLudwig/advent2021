from advent.common import utils
from .day import MarinaBottom, part1


def test_example1():
    input = MarinaBottom.from_str(utils.read_data(25, "test01.txt"))
    expected = 58
    result = input.step()
    assert result == expected


def test_part1():
    input = utils.read_data(25, "test01.txt")
    expected = 58
    result = part1(input)
    assert result == expected
