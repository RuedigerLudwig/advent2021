from typing import Optional
from advent.common import utils


class Command:
    @staticmethod
    def from_str(command: str) -> Optional["Command"]:
        parts = command.split()
        if len(parts) != 2:
            return None

        val = utils.safe_int(parts[1])
        if val is None:
            return None

        match parts[0]:
            case "forward":
                return Command(val, 0)
            case "up":
                return Command(0, -val)
            case "down":
                return Command(0, val)
            case _:
                return None

    def __init__(self, forward: int, down: int) -> None:
        self.forward = forward
        self.down = down

    def __eq__(self, other: object) -> bool:
        if not type(other) is Command:
            return False
        return self.forward == other.forward and self.down == other.down
