import sys

from advent.common import utils
from days import day01, day02, day03, template

days: dict[int, template.Day] = {1: day01, 2: day02, 3: day03}


def output(day: int, part: int, result: int | None) -> None:
    if result is None:
        print("Day {0:02} Part {1}: No Result".format(day, part))
    else:
        print("Day {0:02} Part {1}: {2}".format(day, part, result))


def run(day_num: int, part: int) -> None:
    day = days.get(day_num)
    if day is None:
        print(f"Unknown day {day_num}")
    else:
        day = days[day_num]
        data = utils.read_data(day_num, "input.txt")
        if data is None:
            print(f"Did not find input for day '{day_num}'")
        else:
            match part:
                case 1: output(day_num, 1, day.part1(data))
                case 2: output(day_num, 2, day.part2(data))
                case _: print(f"Unknown part {part}")


def run_from_string(day_str: str) -> None:
    day = utils.safe_int(day_str)
    if day is not None:
        run(day, 1)
        run(day, 2)
    else:
        parts = day_str.split("/")
        if len(parts) != 2:
            print(f"'{day_str}' is not a valid day info")
        else:
            day = utils.safe_int(parts[0])
            part = utils.safe_int(parts[1])
            if day is not None and part is not None:
                run(day, part)
            else:
                print(f"'{day_str}' is not a valid day info")


def main() -> None:
    if len(sys.argv) == 1:
        for day_num in range(1, len(days) + 1):
            run(day_num, 1)
            run(day_num, 2)
    else:
        for arg in sys.argv[1:]:
            run_from_string(arg)


if __name__ == "__main__":
    main()
