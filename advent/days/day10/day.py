from typing import Iterator

day_num = 10


def part1(lines: Iterator[str]) -> int:
    value = 0
    for line in lines:
        try:
            check_chunks(line)
        except CorruptException as err:
            value += err.value
        except IncompleteException:
            pass
    return value


def part2(lines: Iterator[str]) -> int:
    value: list[int] = []
    for line in lines:
        try:
            check_chunks(line)
        except CorruptException:
            pass
        except IncompleteException as err:
            value.append(err.value)
    return sorted(value)[len(value) >> 1]


class CorruptException(Exception):
    def __init__(self, value: int) -> None:
        super().__init__("Corrupt")
        self.value = value


class IncompleteException(Exception):
    def __init__(self, value: int) -> None:
        super().__init__("Incomplete")
        self.value = value


bracket = {"{": "}", "(": ")", "[": "]", "<": ">"}
corrupt_value = {")": 3, "]": 57, "}": 1197, ">": 25137}
incomplete_value = {"(": 1, "[": 2, "{": 3, "<": 4}


def check_chunks(line: str) -> None:
    def check_sub(pos: int) -> int:
        while True:
            # Trusting that there are no correct lines
            if pos >= len(line):
                raise IncompleteException(0)

            start = line[pos]
            if start not in bracket.keys():
                return pos

            try:
                pos = check_sub(pos + 1)
            except IncompleteException as e:
                raise IncompleteException(e.value * 5 + incomplete_value[start])

            end = line[pos]
            if end != bracket[start]:
                raise CorruptException(corrupt_value[end])
            pos += 1
    check_sub(0)
