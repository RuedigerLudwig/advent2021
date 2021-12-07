import sys
from importlib import import_module
from typing import cast

from advent.common import utils
from advent.days.template import Day, ResultType


def output(day: int, part: int, result: ResultType | None) -> None:
    match result:
        case int(value):
            print("Day {0:02} Part {1}: {2}".format(day, part, value))
        case None:
            print("Day {0:02} Part {1}: (No Result)".format(day, part))
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
            day = get_day(int(d))

            run(day, 1)
            run(day, 2)

        case [d, p]:
            day = get_day(int(d))
            part = int(p)

            run(day, part)

        case _:
            raise Exception(f"'{day_str}' is not a valid day description")


def main() -> None:
    try:
        match len(sys.argv):
            case 1:
                try:
                    for day_num in range(1, 25):
                        day = get_day(day_num)
                        run(day, 1)
                        run(day, 2)
                except ModuleNotFoundError:
                    pass
            case 2:
                run_from_string(sys.argv[1])
            case _:
                raise Exception(f"Usage: python {sys.argv[0]} [day[/part]]")
    except Exception as e:
        print(e)


if __name__ == "__main__":
    main()
