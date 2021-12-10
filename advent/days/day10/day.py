from typing import Iterator

day_num = 10


def part1(lines: Iterator[str]) -> int:
    score = 0
    for line in lines:
        try:
            check_chunks(line)
        except CorruptException as err:
            score += err.score
        except IncompleteException:
            pass
    return score


def part2(lines: Iterator[str]) -> int:
    scores: list[int] = []
    for line in lines:
        try:
            check_chunks(line)
        except CorruptException:
            pass
        except IncompleteException as err:
            scores.append(err.score)
    return sorted(scores)[len(scores) >> 1]


class CorruptException(Exception):
    def __init__(self, score: int) -> None:
        super().__init__("Corrupt")
        self.score = score


class EolException(Exception):
    def __init__(self) -> None:
        super().__init__("Eol")

    @property
    def score(self) -> int:
        return 0


class IncompleteException(EolException):
    def __init__(self, score: int) -> None:
        super().__init__()
        self._score = score

    @property
    def score(self) -> int:
        return self._score


bracket = {"{": "}", "(": ")", "[": "]", "<": ">"}
corrupt_score = {")": 3, "]": 57, "}": 1197, ">": 25137}
incomplete_score = {")": 1, "]": 2, "}": 3, ">": 4}


def check_chunks(line: str) -> None:
    def check_sub(pos: int) -> int:
        while True:
            if pos >= len(line):
                raise EolException()

            expected = bracket.get(line[pos])
            if expected is None:
                return pos

            try:
                pos = check_sub(pos + 1)
            except EolException as e:
                raise IncompleteException(e.score * 5 + incomplete_score[expected])

            end = line[pos]
            if end != expected:
                raise CorruptException(corrupt_score[end])
            pos += 1

    try:
        check_sub(0)
    except IncompleteException:
        raise
    except EolException:
        pass
