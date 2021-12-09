from __future__ import annotations

from .command import Command


class Pos:
    def __init__(self, horiz: int, depth: int) -> None:
        self.horiz = horiz
        self.depth = depth

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Pos):
            return False
        return self.horiz == other.horiz and self.depth == other.depth

    def move(self, other: Command) -> Pos:
        return Pos(self.horiz + other.forward, self.depth + other.down)
