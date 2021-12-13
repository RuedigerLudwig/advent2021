from advent.common import utils
from .day import Paper, part1


def test_read():
    input = Paper.from_str(utils.read_data(13, "test01.txt"))
    expected = 18, 2
    result = len(input.points), len(input.folds)
    assert result == expected


def test_fold_once():
    input = Paper.from_str(utils.read_data(13, "test01.txt"))
    expected = 17
    result = len(input.fold_once())
    assert result == expected


def test_part1():
    input = utils.read_data(13, "test01.txt")
    expected = 17
    result = part1(input)
    assert result == expected
