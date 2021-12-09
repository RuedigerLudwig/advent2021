from __future__ import annotations

from typing import Iterator

from .board import Board


class Game:
    @staticmethod
    def from_str(lines: Iterator[str]) -> Game:
        def _read_boards(boards: list[Board]) -> list[Board]:
            try:
                board = Board.from_str(lines)
            except Exception:
                return boards
            return _read_boards(boards + [board])

        drawn = [int(n) for n in next(lines).split(",")]
        next(lines)
        boards = _read_boards([])

        return Game(boards, drawn)

    def __init__(self, boards: list[Board], drawn: list[int]) -> None:
        self.boards: list[Board] = boards
        self.drawn: list[int] = drawn

    def count_boards(self) -> int:
        return len(self.boards)

    def play_game(self) -> tuple[int, Board] | None:
        for drawn in self.drawn:
            for board in self.boards:
                board.draw_number(drawn)
                if board.check_bingo():
                    return drawn, board

    def play_for_last(self) -> tuple[int, Board] | None:
        for drawn in self.drawn:
            for board in self.boards:
                board.draw_number(drawn)
                if board.check_bingo() and len(self.boards) == 1:
                    return drawn, board
            self.boards = [b for b in self.boards if not b.bingo]
