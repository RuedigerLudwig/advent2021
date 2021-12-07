from advent.common import utils

from . import day07


def test_mediam():
    input = day07.Crab([16, 1, 2, 0, 4, 2, 7, 1, 2, 14])
    expected = 2
    result = input.median()
    assert result == expected


def test_cost():
    input = day07.Crab([16, 1, 2, 0, 4, 2, 7, 1, 2, 14])
    expected = 37
    result = input.min_propcost()
    assert result == expected


def test_part1():
    data = utils.read_data(7, "test01.txt")
    expected = 37
    result = day07.part1(data)
    assert result == expected


def test_geocost():
    input = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
    expected = 206
    result = day07.Crab.calc_geocost(input, 2)
    assert result == expected


def test_findmin():
    input = day07.Crab([16, 1, 2, 0, 4, 2, 7, 1, 2, 14])
    expected = 168
    result = input.min_geocost()
    assert result == expected


def test_part2():
    data = utils.read_data(7, "test01.txt")
    expected = 168
    result = day07.part2(data)
    assert result == expected
