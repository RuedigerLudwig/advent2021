from advent.common import utils

from .day import Polymer, part1, part2


def test_read():
    input = Polymer.from_str(utils.read_data(14, "test01.txt"))
    expected = 16
    result = len(input.rules)
    assert result == expected


def test_minmax():
    input = Polymer.from_str(utils.read_data(14, "test01.txt"))
    expected = 1
    result = input.minmax()
    assert result == expected


def test_step():
    input = Polymer.from_str(utils.read_data(14, "test01.txt"))
    expected = {("N", "C"): 1, ("C", "N"): 1, ("N", "B"): 1,
                ("B", "C"): 1, ("C", "H"): 1, ("H", "B"): 1}
    result = input.cook_polymer(1).polymer
    assert result == expected


def test_step2():
    input = Polymer.from_str(utils.read_data(14, "test01.txt"))
    expected = {("N", "B"): 2, ("B", "C"): 2, ("C", "C"): 1,
                ("C", "N"): 1, ("B", "B"): 2, ("C", "B"): 2,
                ("B", "H"): 1, ("H", "C"): 1}
    result = input.cook_polymer(2).polymer
    assert result == expected


def test_steps_10():
    input = Polymer.from_str(utils.read_data(14, "test01.txt"))
    expected = 1588
    result = input.cook_polymer(10).minmax()
    assert result == expected


def test_part1():
    input = utils.read_data(14, "test01.txt")
    expected = 1588
    result = part1(input)
    assert result == expected


def test_part2():
    input = utils.read_data(14, "test01.txt")
    expected = 2188189693529
    result = part2(input)
    assert result == expected
