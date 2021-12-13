import collections
from itertools import islice, pairwise
from typing import Iterator

day_num = 1


def part1(lines: Iterator[str]) -> int:
    return count_increase(convert(lines))


def part2(lines: Iterator[str]) -> int:
    return count_increase(make_blocks(convert(lines), 3))


def convert(lines: Iterator[str]) -> Iterator[int]:
    return (int(line) for line in lines)


def count_increase(lst: Iterator[int]) -> int:
    return sum(1 for a, b in pairwise(lst) if a < b)


def make_blocks(lst: Iterator[int], block_size: int) -> Iterator[int]:
    window = collections.deque(islice(lst, block_size - 1), maxlen=block_size)
    for item in lst:
        window.append(item)
        yield sum(window)
