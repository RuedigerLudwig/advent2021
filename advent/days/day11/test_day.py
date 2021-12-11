from advent.common import utils
from .day import Octopy, part1, part2


def test_step1():
    octopy = Octopy.from_str(utils.read_data(11, "test01.txt"))
    expected = 0
    result = octopy.count_flashes_after_steps(1)
    assert result == expected


def test_step2():
    octopy = Octopy.from_str(utils.read_data(11, "test01.txt"))
    expected = 35
    result = octopy.count_flashes_after_steps(2)
    assert result == expected


def test_step3():
    octopy = Octopy.from_str(utils.read_data(11, "test01.txt"))
    expected = 80
    result = octopy.count_flashes_after_steps(3)
    assert result == expected


def test_step10():
    octopy = Octopy.from_str(utils.read_data(11, "test01.txt"))
    expected = 204
    result = octopy.count_flashes_after_steps(10)
    assert result == expected


def test_step100():
    octopy = Octopy.from_str(utils.read_data(11, "test01.txt"))
    expected = 1656
    result = octopy.count_flashes_after_steps(100)
    assert result == expected


def test_part1():
    data = utils.read_data(11, "test01.txt")
    expected = 1656
    result = part1(data)
    assert result == expected


def test_sync():
    octopy = Octopy.from_str(utils.read_data(11, "test01.txt"))
    expected = 195
    result = octopy.count_steps_to_sync()
    assert result == expected


def test_part2():
    data = utils.read_data(11, "test01.txt")
    expected = 195
    result = part2(data)
    assert result == expected
