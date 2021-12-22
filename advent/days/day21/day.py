from __future__ import annotations

from typing import Iterator

day_num = 21


def part1(lines: Iterator[str]) -> int:
    p1, p2 = from_str(lines)
    _, looser, rolled = play_game(p1, p2)
    return looser * rolled


def part2(lines: Iterator[str]) -> int:
    p1, p2 = from_str(lines)
    winner, _ = play_dirac_game(p1, p2)
    return winner


def from_str(input: Iterator[str]) -> tuple[int, int]:
    def read_line(line: str) -> int:
        match line.split(":"):
            case [_, num]:
                return int(num.strip())
            case _:
                raise Exception
    p1 = read_line(next(input))
    p2 = read_line(next(input))

    return p1, p2


def play_game(start1: int, start2: int):
    die = 2
    rolled = 0
    pos1 = start1
    pos2 = start2
    score1 = 0
    score2 = 0
    player1 = True
    while score1 < 1000 and score2 < 1000:
        add = (die * 3 - 1) % 100 + 1
        if player1:
            pos1 = (pos1 + add - 1) % 10 + 1
            score1 += pos1
        else:
            pos2 = (pos2 + add - 1) % 10 + 1
            score2 += pos2
        die = (die + 2 % 100) + 1
        rolled += 3
        player1 = not player1

    if score1 >= 1000:
        return score1, score2, rolled
    else:
        return score2, score1, rolled


outcome = [1, 3, 6, 7, 6, 3, 1]


def one_round(results: dict[tuple[int, int], int]) -> tuple[dict[tuple[int, int], int], int]:
    win = 0
    next_results: dict[tuple[int, int], int] = {}
    for (prev_pos, prev_score), count in results.items():
        for rolled, prob in enumerate(outcome, 3):
            next_pos = (prev_pos + rolled - 1) % 10 + 1
            next_score = prev_score + next_pos
            if next_score >= 21:
                win += count * prob
            else:
                prev = next_results.get((next_pos, next_score), 0)
                next_results[(next_pos, next_score)] = prev + count * prob
    return next_results, win


def play_dirac_game(start1: int, start2: int):
    score1: dict[tuple[int, int], int] = {(start1, 0): 1}
    score2: dict[tuple[int, int], int] = {(start2, 0): 1}
    win1 = 0
    win2 = 0
    player1 = True

    while score1 and score2:
        if player1:
            score1, win = one_round(score1)
            win1 += win * sum(score2.values())
        else:
            score2, win = one_round(score2)
            win2 += win * sum(score1.values())
        player1 = not player1

    if win1 > win2:
        return win1, win2
    else:
        return win2, win1
