from advent.common import utils

from .day import Layout, part1, part2


def test_move_all():
    input = Layout.from_str(utils.read_data(23, "test01.txt"))
    expected = 12521
    result = input.find_path()
    assert result == expected


def test_print():
    input = Layout.from_str(utils.read_data(23, "test01.txt"))
    str(input)
    assert True


def test_part1():
    input = utils.read_data(23, "test01.txt")
    expected = 12521
    result = part1(input)
    assert result == expected


def test_part2():
    input = utils.read_data(23, "test01.txt")
    expected = 44169
    result = part2(input)
    assert result == expected
