from advent.common import utils
from .day import Cave, part1, part2


def test_lowpoints():
    input = Cave.from_str(utils.read_data(9, "test01.txt"))
    expected = {(1, 0), (9, 0), (2, 2), (6, 4)}
    result = input.find_lowpoints()
    assert result == expected


def test_risklevel():
    input = Cave.from_str(utils.read_data(9, "test01.txt"))
    expected = 15
    result = input.get_cave_risklevel()
    assert result == expected


def test_part1():
    data = utils.read_data(9, "test01.txt")
    expected = 15
    result = part1(data)
    assert result == expected


def test_basin_size():
    input = Cave.from_str(utils.read_data(9, "test01.txt"))
    expected = 3
    result = input.get_basin_size((1, 0))
    assert result == expected


def test_all_basin_sizes():
    input = Cave.from_str(utils.read_data(9, "test01.txt"))
    expected = [14, 9, 9, 3]
    result = input.get_sorted_basin_sizes()
    assert result == expected


def test_part2():
    data = utils.read_data(9, "test01.txt")
    expected = 1134
    result = part2(data)
    assert result == expected
