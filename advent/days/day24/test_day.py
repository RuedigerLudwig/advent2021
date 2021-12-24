from advent.common import utils
from .classic_monad import ClassicMonad


def test_neg():
    monad = ClassicMonad.from_str(utils.read_data(24, "test01.txt"))
    input = "5"
    expected = [0, -5, 0, 0]
    result = monad.follow_instructions(input)
    assert result == expected


def test_cmp1():
    monad = ClassicMonad.from_str(utils.read_data(24, "test02.txt"))
    input = "39"
    expected = [0, 9, 0, 1]
    result = monad.follow_instructions(input)
    assert result == expected


def test_cmp2():
    monad = ClassicMonad.from_str(utils.read_data(24, "test03.txt"))
    input = "9"
    expected = [1, 0, 0, 1]
    result = monad.follow_instructions(input)
    assert result == expected
