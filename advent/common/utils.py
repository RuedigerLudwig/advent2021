from pathlib import Path, PurePath
from typing import Callable, Iterator, TypeVar

T = TypeVar("T")


def read_data(day: int, file_name: str) -> Iterator[str]:
    """
    Returns an iterator over the content of the mentioned file
    All lines are striped of an eventual trailing "\n" their
    """
    with open(
        Path.cwd()
        / PurePath("advent/days/day{0:02}/data".format(day))
        / PurePath(file_name),
        "rt",
    ) as file:
        while True:
            line = file.readline()
            if line:
                yield line if line[-1] != "\n" else line[:-1]
            else:
                return


def split_set(full_set: set[T], predicate: Callable[[T], bool]) -> tuple[set[T], set[T]]:
    """ Splits a set in two sorted by the predicate """
    true_set: set[T] = set()
    false_set: set[T] = set()
    for item in full_set:
        (true_set if predicate(item) else false_set).add(item)
    return true_set, false_set
