from advent.common import utils

from . import day


def test_parsing():
    input = "3,4,3,1,2"
    expected = [0, 1, 1, 2, 1, 0, 0, 0, 0]
    result = day.Swarm.from_str(input).swarm
    assert result == expected


def test_day():
    input = day.Swarm([0, 1, 1, 2, 1, 0, 0, 0, 0])
    expected = [1, 1, 2, 1, 0, 0, 0, 0, 0]
    result = input.age(1).swarm
    assert result == expected


def test_day2():
    input = day.Swarm([0, 1, 1, 2, 1, 0, 0, 0, 0])
    expected = [1, 2, 1, 0, 0, 0, 1, 0, 1]
    result = input.age(2).swarm
    assert result == expected


def test_day80():
    input = day.Swarm([0, 1, 1, 2, 1, 0, 0, 0, 0])
    expected = 5934
    result = input.age(80).size()
    assert result == expected


def test_day256():
    input = day.Swarm([0, 1, 1, 2, 1, 0, 0, 0, 0])
    expected = 26984457539
    result = input.age(256).size()
    assert result == expected


def test_part1():
    data = utils.read_data(6, "test01.txt")
    expected = 5934
    result = day.part1(data)
    assert result == expected


def test_part2():
    data = utils.read_data(6, "test01.txt")
    expected = 26984457539
    result = day.part2(data)
    assert result == expected
