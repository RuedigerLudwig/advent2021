from advent.common import utils
from .day import CaveSystem, part1, part2


def test_day():
    input = utils.read_data(12, "test01.txt")
    expected = {
        "start": {"A", "b"},
        "c": {"A"},
        "d": {"b"},
        "A": {"start", "c", "b", "end"},
        "b": {"start", "A", "d", "end"},
        "end": {"A", "b"}
    }
    result = CaveSystem.from_str(input)
    assert result.system == expected


def test_all_paths():
    input = CaveSystem.from_str(utils.read_data(12, "test01.txt"))
    expected = 10
    result = input.all_paths()
    assert result == expected


def test_part1_1():
    input = utils.read_data(12, "test01.txt")
    expected = 10
    result = part1(input)
    assert result == expected


def test_part1_2():
    input = utils.read_data(12, "test02.txt")
    expected = 19
    result = part1(input)
    assert result == expected


def test_part1_3():
    input = utils.read_data(12, "test03.txt")
    expected = 226
    result = part1(input)
    assert result == expected


def test_all_paths_2():
    input = CaveSystem.from_str(utils.read_data(12, "test01.txt"))
    expected = 36
    result = input.all_paths2()
    assert result == expected


def test_part2_1():
    input = utils.read_data(12, "test01.txt")
    expected = 36
    result = part2(input)
    assert result == expected


def test_part2_2():
    input = utils.read_data(12, "test02.txt")
    expected = 103
    result = part2(input)
    assert result == expected


def test_part2_3():
    input = utils.read_data(12, "test03.txt")
    expected = 3509
    result = part2(input)
    assert result == expected
