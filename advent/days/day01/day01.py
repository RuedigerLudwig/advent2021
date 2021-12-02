def part1(lines: list[str]) -> int:
    return count_increase(convert(lines))


def part2(lines: list[str]) -> int:
    return count_increase(make_blocks(convert(lines), 3))


def convert(lines: list[str]) -> list[int]:
    return [int(line) for line in lines]


def count_increase(lst: list[int]) -> int:
    return len([i for i in range(1, len(lst)) if lst[i - 1] < lst[i]])


def make_blocks(lst: list[int], block_size: int) -> list[int]:
    return [sum(lst[i : i + block_size]) for i in range(0, len(lst) - block_size + 1)]
