from advent.common import utils

from .day import (A1, B1, C1, H1, H2, H3, H4, H5, H6, H7, AmphipodHome, B, part1,
                  part2)


def test_get_possible_moves():
    input = AmphipodHome.from_str(utils.read_data(23, "test01.txt"))
    expected = {(H1, 30), (H2, 20), (H3, 20), (H4, 40), (H5, 60), (H6, 80), (H7, 90)}
    result = set(input.possible_paths_for(A1, B))
    assert result == expected


def test_get_possible_moves3():
    input = AmphipodHome.from_str(utils.read_data(23, "test01.txt"))
    input = input.move(C1, H3)
    input = input.move(B1, C1)

    expected: set[tuple[str, int]] = set()
    result = set(input.possible_paths_for(H3, B))
    assert result == expected


def test_move_all():
    input = AmphipodHome.from_str(utils.read_data(23, "test01.txt"))
    expected = 12521
    result = input.find_path()
    assert result == expected


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
