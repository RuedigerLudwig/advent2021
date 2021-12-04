from pathlib import Path, PurePath
from typing import Iterable, TypeVar, Callable

T = TypeVar("T")


def read_data(day: int, file: str) -> list[str]:
    with open(
        Path.cwd()
        / PurePath("advent/days/day{0:02}/data".format(day))
        / PurePath(file),
        "rt",
    ) as f:
        return f.readlines()


def some_filter(lst: Iterable[T | None]) -> Iterable[T]:
    return (item for item in lst if item is not None)


def count(lst: Iterable[T], check: Callable[[T], bool]) -> int:
    return sum(1 for t in lst if check(t))


def safe_int(s: str) -> int | None:
    try:
        return int(s)
    except ValueError:
        return None


def safe_get(lst: list[T], pos: int, default: T) -> T:
    try:
        return lst[pos]
    except IndexError:
        return default
