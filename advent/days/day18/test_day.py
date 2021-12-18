from advent.common import utils

from .day import part1, part2
from .number import SnailInt, SnailNumber, SnailPair


def test_parse1():
    input = "[1,2]"
    expected = SnailPair(SnailInt(1), SnailInt(2))
    result = SnailNumber.from_str(input)
    assert result == expected


def test_parse1a():
    input = "[10,12]"
    expected = SnailPair(SnailInt(10), SnailInt(12))
    result = SnailNumber.from_str(input)
    assert result == expected


def test_parse2():
    input = "[[1,9],[8,5]]"
    expected = SnailPair(SnailPair(SnailInt(1), SnailInt(9)), SnailPair(SnailInt(8), SnailInt(5)))
    result = SnailNumber.from_str(input)
    assert result == expected


def test_max_level():
    input = SnailNumber.from_str("[[[[[9,8],1],2],3],4]")
    expected = 5
    result = input.max_level()
    assert result == expected


def test_single_explode1():
    input = SnailNumber.from_str("[[[[[9,8],1],2],3],4]")
    expected = SnailNumber.from_str("[[[[0,9],2],3],4]")
    result = input.single_explode()
    assert result == expected


def test_single_explode2():
    input = SnailNumber.from_str("[[3,[2,[1,[7,3]]]],[6,[5,[4,[3,2]]]]]")
    expected = SnailNumber.from_str("[[3,[2,[8,0]]],[9,[5,[4,[3,2]]]]]")
    result = input.single_explode()
    assert result == expected


def test_single_explode3():
    input = SnailNumber.from_str("[[[[0,7],4],[7,[[8,4],9]]],[1,1]]")
    expected = SnailNumber.from_str("[[[[0,7],4],[15,[0,13]]],[1,1]]")
    result = input.single_explode()
    assert result == expected


def test_split():
    input = SnailNumber.from_str("[[[[0,7],4],[15,[0,13]]],[1,1]]")
    expected = SnailNumber.from_str("[[[[0,7],4],[[7,8],[0,13]]],[1,1]]")
    result = input.single_split()
    assert result == expected


def test_reduce():
    input = SnailNumber.from_str("[[[[[4,3],4],4],[7,[[8,4],9]]],[1,1]]")
    expected = SnailNumber.from_str("[[[[0,7],4],[[7,8],[6,0]]],[8,1]]")
    result = input.reduce()
    assert result == expected


def test_add_lines1():
    input = (SnailNumber.from_str(line) for line in utils.read_data(18, "test01.txt"))
    expected = SnailNumber.from_str("[[[[1,1],[2,2]],[3,3]],[4,4]]")
    result = SnailNumber.add_all(input)
    assert result == expected


def test_add_lines2():
    input = (SnailNumber.from_str(line) for line in utils.read_data(18, "test02.txt"))
    expected = SnailNumber.from_str("[[[[3,0],[5,3]],[4,4]],[5,5]]")
    result = SnailNumber.add_all(input)
    assert result == expected


def test_add_lines3():
    input = (SnailNumber.from_str(line) for line in utils.read_data(18, "test03.txt"))
    expected = SnailNumber.from_str("[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]")
    result = SnailNumber.add_all(input)
    assert result == expected


def test_add_magnitude1():
    input = SnailNumber.from_str("[[1,2],[[3,4],5]]")
    expected = 143
    result = input.magnitude()
    assert result == expected


def test_add_magnitude2():
    input = SnailNumber.from_str("[[[[6,6],[7,6]],[[7,7],[7,0]]],[[[7,7],[7,7]],[[7,8],[9,9]]]]")
    expected = 4140
    result = input.magnitude()
    assert result == expected


def test_add_magnitude3():
    input = (SnailNumber.from_str(line) for line in utils.read_data(18, "test03.txt"))
    expected = 4140
    result = SnailNumber.add_all(input).magnitude()
    assert result == expected


def test_add_part1():
    input = utils.read_data(18, "test03.txt")
    expected = 4140
    result = part1(input)
    assert result == expected


def test_find_largest():
    input = (SnailNumber.from_str(line) for line in utils.read_data(18, "test03.txt"))
    expected = 3993
    result = SnailNumber.find_largest(input)
    assert result == expected


def test_add_part2():
    input = utils.read_data(18, "test03.txt")
    expected = 3993
    result = part2(input)
    assert result == expected
