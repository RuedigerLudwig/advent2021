from .day import Analyzer, part1, part2
from advent.common import utils


def test_count_easy():
    input = Analyzer.from_str(
        "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf")
    expected = 0
    result = input.count_easy()
    assert result == expected


def test_multi():
    input = [Analyzer.from_str(line) for line in utils.read_data(8, "test01.txt")]
    expected = 26
    result = sum(out.count_easy() for out in input)
    assert result == expected


def test_part1():
    data = utils.read_data(8, "test01.txt")
    expected = 26
    result = part1(data)
    assert result == expected


def test_get_output():
    input = Analyzer.from_str(
        "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf")
    expected = 5353
    result = input.real_output()
    assert result == expected


def test_part2():
    data = utils.read_data(8, "test01.txt")
    expected = 61229
    result = part2(data)
    assert result == expected
