day_num = 8


def part1(lines: list[str]) -> int:
    return sum(Segment.from_str(line).count_easy() for line in lines)


def part2(lines: list[str]) -> int:
    return sum(Segment.from_str(line).real_output() for line in lines)


class Segment:
    @staticmethod
    def from_str(line: str) -> "Segment":
        parts = line.strip().split("|")
        if len(parts) != 2:
            raise Exception("Need exactly two parts")
        pattern = parts[0].split()
        if len(pattern) != 10:
            raise Exception("Unknown pattern")
        output = parts[1].split()
        return Segment(pattern, output)

    def __init__(self, pattern: list[str], output: list[str]):
        self.pattern = ["".join(sorted(p)) for p in pattern]
        self.output = ["".join(sorted(o)) for o in output]

    def count_easy(self) -> int:
        return sum(1 for digit in self.output if len(digit) in [2, 3, 4, 7])

    def analyze(self) -> dict[str, int]:
        def singleton(lst: list[str]) -> str:
            if len(lst) != 1:
                raise Exception("Did not get exactly one result")
            return lst[0]

        all_bars = "abcdefg"

        one = singleton([p for p in self.pattern if len(p) == 2])
        four = singleton([p for p in self.pattern if len(p) == 4])
        seven = singleton([p for p in self.pattern if len(p) == 3])
        eight = singleton([p for p in self.pattern if len(p) == 7])

        six_bars = [p for p in self.pattern if len(p) == 6]
        six = singleton([p for p in six_bars if any(bar not in p for bar in one)])
        upper_right_bar = singleton([b for b in all_bars if b not in six])

        five_bars = [p for p in self.pattern if len(p) == 5]
        three = singleton([p for p in five_bars if all(bar in p for bar in one)])
        two = singleton([p for p in five_bars if p != three and upper_right_bar in p])
        five = singleton([p for p in five_bars if upper_right_bar not in p])

        horiz_bars = [b for b in all_bars if all(b in p for p in five_bars)]
        zero = singleton([p for p in six_bars if any(b not in p for b in horiz_bars)])
        nine = singleton([p for p in six_bars if p
                         != six and all(b in p for b in horiz_bars)])

        return {zero: 0, one: 1, two: 2, three: 3, four: 4, five: 5, six: 6, seven: 7, eight: 8, nine: 9}

    def real_output(self) -> int:
        def value(lst: list[int], pos: int, factor: int, result: int) -> int:
            if pos < 0:
                return result
            return value(lst, pos - 1, factor * 10, result + factor * lst[pos])

        pmap = self.analyze()
        digits = [pmap[digit] for digit in self.output]
        return value(digits, len(digits) - 1, 1, 0)
