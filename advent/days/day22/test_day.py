from advent.common import utils

from .day import Command, Cube, part1, part2


def test_render1():
    input = "on x=10..12,y=11..12,z=12..12"
    expected = Command(0, True, Cube((10, 12), (11, 12), (12, 12)))
    result = Command.from_str(input, 0)
    assert result == expected


def test_render2():
    input = "off x=9..11,y=9..12,z=9..13"
    expected = Command(0, False, Cube((9, 11), (9, 12), (9, 13)))
    result = Command.from_str(input, 0)
    assert result == expected


def test_complex():
    input = [Command.from_str(c, 0) for c in utils.read_data(22, "test01.txt")]
    expected = 590784
    result = Command.merge_small(input)
    assert result == expected


def test_part1():
    input = utils.read_data(22, "test01.txt")
    expected = 590784
    result = part1(input)
    assert result == expected


def test_big():
    input = [Command.from_str(c, n) for n, c in enumerate(utils.read_data(22, "test02.txt"))]
    expected = 2758514936282235
    result = Command.merge_big(input)
    assert result == expected


def test_part2():
    input = utils.read_data(22, "test02.txt")
    expected = 2758514936282235
    result = part2(input)
    assert result == expected
