from __future__ import annotations

from typing import Iterator


class Board:
    @staticmethod
    def from_str(lines: Iterator[str]) -> Board:
        numbers: list[list[int]] = []
        for _ in range(5):
            number_line = [int(n) for n in next(lines).split()]
            if len(number_line) != 5:
                raise Exception("Wrong amount of numbers in line")
            numbers.append(number_line)

        try:
            next(lines)
        except StopIteration:
            pass

        return Board(numbers)

    def __init__(self, numbers: list[list[int]]) -> None:
        self.numbers: list[int | None] = [n for lst in numbers for n in lst]
        self.bingo = False

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Board):
            return False
        return (len(self.numbers) == len(other.numbers)
                and all(a == b for a, b in zip(self.numbers, other.numbers)))

    def draw_number(self, number: int) -> None:
        if number in self.numbers and not self.bingo:
            self.numbers = [n if n != number else None for n in self.numbers]

            self.bingo = any(
                all(self.numbers[row * 5 + col] is None for col in range(5))
                or all(self.numbers[row + col * 5] is None for col in range(5))
                for row in range(5)
            )

    def check_bingo(self) -> bool:
        return self.bingo

    def get_num_value(self) -> int:
        return sum(n for n in self.numbers if n is not None)
