import sys
from importlib import import_module
from typing import cast

from advent.common import utils
from advent.days.template import Day, ResultType


def output(day: int, part: int, result: ResultType | None) -> None:
    match result:
        case None:
            print("Day {0:02} Part {1}: (No Result)".format(day, part))
        case int(value):
            print("Day {0:02} Part {1}: {2}".format(day, part, value))
        case _:
            print("Day {0:02} Part {1}: (Unknown result type)".format(day, part))


def get_day(day_num: int) -> Day:
    day = import_module("advent.days.day{0:02}".format(day_num))
    return cast(Day, day)


def run(day: Day, part: int) -> None:
    data = utils.read_data(day.day_num, "input.txt")
    match part:
        case 1: output(day.day_num, 1, day.part1(data))
        case 2: output(day.day_num, 2, day.part2(data))
        case _: raise Exception(f"Unknown part {part}")


def run_from_string(day_str: str) -> None:
    match day_str.split("/"):
        case [d]:
            day_num = utils.safe_int(d)
            if day_num is None:
                raise Exception(f"'{day_str}' is not a valid day info")
            day = get_day(day_num)

            run(day, 1)
            run(day, 2)

        case [d, p]:
            day_num = utils.safe_int(d)
            part = utils.safe_int(p)
            if day_num is None or part is None:
                raise Exception(f"'{day_str}' is not a valid day info")

            day = get_day(day_num)
            run(day, part)

        case _:
            raise Exception(f"'{day_str}' is not a valid day info")


def main() -> None:
    try:
        if len(sys.argv) == 1:
            try:
                for day_num in range(1, 25):
                    day = get_day(day_num)
                    run(day, 1)
                    run(day, 2)
            except ModuleNotFoundError:
                pass
        else:
            for arg in sys.argv[1:]:
                run_from_string(arg)
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
