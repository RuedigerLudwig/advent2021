from __future__ import annotations

from .command import Command


class Aim:
    def __init__(self, horiz: int, aim: int, depth: int) -> None:
        self.horiz = horiz
        self.aim = aim
        self.depth = depth

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Aim):
            return False
        return self.horiz == other.horiz and self.aim == other.aim and self.depth == other.depth

    def move(self, other: Command) -> Aim:
        return Aim(self.horiz + other.forward, self.aim
                   + other.down, self.depth + other.forward * self.aim)
