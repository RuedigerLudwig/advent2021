import pytest
from advent.common import utils

from .day import Chunk, CorruptException, IncompleteException, part1, part2


def test_correct_chunk():
    input = "[{}()]"
    expected = "[{}()]"
    result = str(Chunk.from_str(input)[0])
    assert result == expected


def test_corrupt_chunk():
    input = "{([(<{}[<>[]}>{[]{[(<()>"
    expected = 1197
    with pytest.raises(CorruptException) as err:
        Chunk.from_str(input)
    assert err.value.score == expected


def test_part1():
    data = utils.read_data(10, "test01.txt")
    expected = 26397
    result = part1(data)
    assert result == expected


def test_incomplete_chunk():
    input = "[({(<(())[]>[[{[]{<()<>>"
    expected = 288957
    with pytest.raises(IncompleteException) as err:
        Chunk.from_str(input)
    assert err.value.score == expected


def test_part2():
    data = utils.read_data(10, "test01.txt")
    expected = 288957
    result = part2(data)
    assert result == expected
