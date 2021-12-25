from advent.common import utils
from advent.days.day19.scanner import Matrix, Vector

from .day import Scanner, part1, part2


def test_parse1():
    input = Scanner.from_str(utils.read_data(19, "test01.txt"))
    expected = 25
    result = len(input.beacons)
    assert result == expected


def test_parse2():
    input = Scanner.from_iterator(utils.read_data(19, "test01.txt"))
    expected = 5
    result = len(input)
    assert result == expected


def test_part1():
    input = utils.read_data(19, "test01.txt")
    expected = 79
    result = part1(input)
    assert result == expected


def test_part2():
    input = utils.read_data(19, "test01.txt")
    expected = 3621
    result = part2(input)
    assert result == expected


def test_overlap01():
    input = Scanner.from_iterator(utils.read_data(19, "test01.txt"))
    matched = list(Scanner.match_all([input[0], input[1]]))
    expected: set[Vector] = {Vector((-618, -824, -621)),
                             Vector((-537, -823, -458)),
                             Vector((-447, -329, 318)),
                             Vector((404, -588, -901)),
                             Vector((544, -627, -890)),
                             Vector((528, -643, 409)),
                             Vector((-661, -816, -575)),
                             Vector((390, -675, -793)),
                             Vector((423, -701, 434)),
                             Vector((-345, -311, 381)),
                             Vector((459, -707, 401)),
                             Vector((-485, -357, 347))}
    result = matched[0].beacons.keys() & matched[1].beacons.keys()
    assert result == expected


def test_overlap14():
    input = Scanner.from_iterator(utils.read_data(19, "test01.txt"))
    matched = list(Scanner.match_all([input[0], input[1], input[4]]))
    expected = {Vector((0, 0, 0)), Vector((68, -1246, -43)), Vector((-20, -1133, 1061))}
    result = {s.origin for s in matched}
    assert result == expected


def test_mul():
    vector = Vector((1, 2, 3))
    matrix = Matrix((Vector((0, 0, 1)), Vector((-1, 0, 0)), Vector((0, 2, 0))))
    expected = Vector((3, -1, 4))
    result = matrix * vector
    assert result == expected
