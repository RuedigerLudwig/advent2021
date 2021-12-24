from __future__ import annotations

from typing import Iterable, Iterator

from .instruction import Instruction, Operation


class ReverseMonad:
    @staticmethod
    def from_str(lines: Iterator[str]) -> ReverseMonad:
        instructions = [Instruction.from_str(line) for line in lines]
        return ReverseMonad(instructions)

    def __init__(self, instructions: list[Operation]):
        def extract_params():
            result: list[list[int]] = []
            current: list[int] = []
            pos = 0
            for instruction in instructions:
                if instruction.is_input():
                    pos = 1
                    current = []
                else:
                    match pos:
                        case 4 | 5:
                            current.append(instruction.value())
                        case 15:
                            current.append(instruction.value())
                            result.append(current)
                    pos += 1
            return result

        self.params = extract_params()

    def find_number(self, number: int, pos: int, old_value: int,
                    numrange: Iterable[int]) -> int | None:
        def _calc(value: int, input: int, divisor: int, comparer: int, added: int) -> int:
            to_compare = (value % 26) + comparer
            if to_compare != input:
                multiplier = 26
                adder = input + added
            else:
                multiplier = 1
                adder = 0

            return (value // divisor) * multiplier + adder

        if pos == len(self.params):
            return number if old_value == 0 else None

        if self.params[pos][0] == 26:
            required = old_value % 26 + self.params[pos][1]
            if required not in range(1, 10):
                return None
            new_value = _calc(old_value, required, *self.params[pos])
            return self.find_number(number * 10 + required, pos + 1, new_value, numrange)
        else:
            for num in numrange:
                new_value = _calc(old_value, num, *self.params[pos])
                result = self.find_number(number * 10 + num, pos + 1, new_value, numrange)
                if result is not None:
                    return result
            return None

    def try_down(self):
        result = self.find_number(0, 0, 0, range(9, 0, -1))
        if not result:
            raise Exception
        return result

    def try_up(self):
        result = self.find_number(0, 0, 0, range(1, 10))
        if not result:
            raise Exception
        return result
