

class Command:
    @staticmethod
    def from_str(command: str) -> "Command":
        match command.split():
            case ['forward', value]:
                return Command(int(value), 0)
            case ['up', value]:
                return Command(0, -int(value))
            case ['down', value]:
                return Command(0, int(value))
            case _:
                raise Exception(f"Unknown command {command}")

    def __init__(self, forward: int, down: int) -> None:
        self.forward = forward
        self.down = down

    def __eq__(self, other: object) -> bool:
        if not type(other) is Command:
            return False
        return self.forward == other.forward and self.down == other.down
