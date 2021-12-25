from __future__ import annotations

from typing import Iterator

from .scanner import Scanner

day_num = 19


def part1(lines: Iterator[str]) -> int:
    scanner = Scanner.from_iterator(lines)
    result = Scanner.merge_all(scanner)
    return len(result)


def part2(lines: Iterator[str]) -> int:
    scanner = Scanner.from_iterator(lines)
    return Scanner.max_distance(scanner)
