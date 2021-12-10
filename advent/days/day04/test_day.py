from advent.common import utils

from . import day
from .board import Board
from .game import Game


def test_read_board():
    data = utils.read_data(4, "board1.txt")
    expected = Board([[22, 13, 17, 11, 0],
                      [8, 2, 23, 4, 24],
                      [21, 9, 14, 16, 7],
                      [6, 10, 3, 18, 5],
                      [1, 12, 20, 15, 19]])
    result = Board.from_str(data)
    assert result == expected


def test_draw_one():
    data = utils.read_data(4, "board1.txt")
    board = Board.from_str(data)
    expected = False
    board.draw_number(7)
    result = board.check_bingo()
    assert result == expected


def test_draw_to_win_row():
    data = utils.read_data(4, "board3.txt")
    board = Board.from_str(data)
    expected = True
    for n in [7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24]:
        board.draw_number(n)
    result = board.check_bingo()
    assert result == expected


def test_draw_to_win_col():
    data = utils.read_data(4, "board1.txt")
    board = Board.from_str(data)
    expected = True
    for n in [7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24, 19]:
        board.draw_number(n)
    result = board.check_bingo()
    assert result == expected


def test_read_boards():
    data = utils.read_data(4, "test01.txt")
    game = Game.from_str(data)
    expected = 3
    result = game.count_boards()
    assert result == expected


def test_read_drawn():
    data = utils.read_data(4, "test01.txt")
    game = Game.from_str(data)
    expected = [7, 4, 9, 5, 11, 17, 23, 2, 0, 14, 21, 24, 10,
                16, 13, 6, 15, 25, 12, 22, 18, 20, 8, 19, 3, 26, 1]
    result = list(game.drawn)
    assert result == expected


def test_play_game():
    data = utils.read_data(4, "test01.txt")
    game = Game.from_str(data)
    expected = 24, 188
    result = game.play_game()
    assert result is not None
    assert result[0], result[1].get_num_value() == expected


def test_part1():
    data = utils.read_data(4, "test01.txt")
    expected = 4512
    result = day.part1(data)
    assert result == expected


def test_play_for_last():
    data = utils.read_data(4, "test01.txt")
    game = Game.from_str(data)
    expected = 13, 148
    result = game.play_for_last()
    assert result is not None
    assert result[0], result[1].get_num_value() == expected


def test_part2():
    data = utils.read_data(4, "test01.txt")
    expected = 1924
    result = day.part2(data)
    assert result == expected
