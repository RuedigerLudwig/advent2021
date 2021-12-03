import sys

from days import day01, day02, day03, template

from advent.common import utils

days: dict[int, template.Day] = {1: day01, 2: day02, 3: day03}


def output(day: int, part: int, result: template.ResultType | None) -> None:
    if result is None:
        print("Day {0:02} Part {1}: (No Result)".format(day, part))
    else:
        print("Day {0:02} Part {1}: {2}".format(day, part, result))


def run(day_num: int, part: int) -> None:
    day = days.get(day_num)
    if day is None:
        raise Exception(f"Unknown day {day_num}")

    data = utils.read_data(day_num, "input.txt")
    if data is None:
        raise Exception(f"Did not find input for day '{day_num}'")

    match part:
        case 1: output(day_num, 1, day.part1(data))
        case 2: output(day_num, 2, day.part2(data))
        case _: raise Exception(f"Unknown part {part}")


def run_from_string(day_str: str) -> None:
    match day_str.split("/"):
        case [d]:
            day = utils.safe_int(d)
            if day is None:
                raise Exception(f"'{day_str}' is not a valid day info")

            run(day, 1)
            run(day, 2)

        case [d, p]:
            day = utils.safe_int(d)
            part = utils.safe_int(p)
            if day is None or part is None:
                raise Exception(f"'{day_str}' is not a valid day info")

            run(day, part)

        case _:
            raise Exception(f"'{day_str}' is not a valid day info")


def main() -> None:
    try:
        if len(sys.argv) == 1:
            for day_num in range(1, len(days) + 1):
                run(day_num, 1)
                run(day_num, 2)
        else:
            for arg in sys.argv[1:]:
                run_from_string(arg)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
