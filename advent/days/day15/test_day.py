from advent.common import utils
from .day import Cave, part1, part2


def test_path():
    input = Cave.from_str(utils.read_data(15, "test01.txt"))
    expected = 40
    result = input.find_path1()
    assert result == expected


def test_part1():
    input = utils.read_data(15, "test01.txt")
    expected = 40
    result = part1(input)
    assert result == expected


def test_path2():
    input = Cave.from_str(utils.read_data(15, "test01.txt"))
    expected = 315
    result = input.find_path2()
    assert result == expected


def test_adjacent2():
    input = Cave.from_str(utils.read_data(15, "test01.txt"))
    expected = {((49, 47), 8), ((48, 48), 1), ((49, 49), 9)}
    result = set(input.adjacent2((49, 48)))
    assert result == expected


def test_part2():
    input = utils.read_data(15, "test01.txt")
    expected = 315
    result = part2(input)
    assert result == expected
