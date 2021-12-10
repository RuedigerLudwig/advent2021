from __future__ import annotations

from typing import Generator, Iterator

from advent.common import CharProvider
from advent.common.provider import EofException

day_num = 10


def part1(lines: Iterator[str]) -> int:
    score = 0
    for line in lines:
        try:
            Chunk.from_str(line)
        except CorruptException as err:
            score += err.score
        except IncompleteException:
            pass
    return score


def part2(lines: Iterator[str]) -> int:
    scores: list[int] = []
    for line in lines:
        try:
            Chunk.from_str(line)
        except CorruptException:
            pass
        except IncompleteException as err:
            scores.append(err.score)
    return sorted(scores)[len(scores) >> 1]


class CorruptException(Exception):
    def __init__(self, score: int) -> None:
        self.score = score


class IncompleteException(Exception):
    def __init__(self, score: int) -> None:
        self.score = score


class Chunk():
    bracket = {"{": "}", "(": ")", "[": "]", "<": ">"}
    corrupt_score = {")": 3, "]": 57, "}": 1197, ">": 25137}
    incomplete_score = {"(": 1, "[": 2, "{": 3, "<": 4}

    @staticmethod
    def from_str(line: str) -> list[Chunk]:
        return Chunk.chunk_list(CharProvider(line))

    @staticmethod
    def single_chunk(provider: CharProvider) -> Chunk:
        start = provider.get()
        try:
            sub = Chunk.chunk_list(provider)
            end = provider.get()
            if end != Chunk.bracket[start]:
                raise CorruptException(Chunk.corrupt_score[end])
            return Chunk(start, sub)
        except EofException:
            raise IncompleteException(Chunk.incomplete_score[start]) from None
        except IncompleteException as e:
            raise IncompleteException(e.score * 5 + Chunk.incomplete_score[start]) from None

    @staticmethod
    def chunk_generator(provider: CharProvider) -> Generator[Chunk, None, None]:
        while not provider.finished():
            if provider.peek() not in Chunk.bracket.keys():
                return None
            yield Chunk.single_chunk(provider)

    @staticmethod
    def chunk_list(provider: CharProvider) -> list[Chunk]:
        return list(Chunk.chunk_generator(provider))

    def __init__(self, start: str, sub: list[Chunk]):
        self.start = start
        self.sub = sub

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Chunk):
            return False
        return self.start == other.start and self.sub == other.sub

    def __repr__(self) -> str:
        return f"{self.start}{''.join(repr(s) for s in  self.sub)}{Chunk.bracket[self.start]}"
