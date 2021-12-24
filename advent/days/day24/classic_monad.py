from __future__ import annotations

from typing import Iterator

from .instruction import Instruction, Operation


class ClassicMonad:
    @staticmethod
    def from_str(lines: Iterator[str]) -> ClassicMonad:
        instructions = [Instruction.from_str(line) for line in lines]
        return ClassicMonad(instructions)

    def __init__(self, instructions: list[Operation]):
        self.instructions = instructions

    def follow_instructions(self, str_input: str) -> list[int]:
        it = (int(d) for d in str_input)
        registers = [0] * 4
        for instruction in self.instructions:
            registers = instruction(registers, it)
            print(f"{instruction.name()}\t{registers}\t{input}")
        return registers
