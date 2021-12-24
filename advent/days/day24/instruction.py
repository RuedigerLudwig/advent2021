import abc
from typing import Callable, Iterator


class Operation(abc.ABC):
    @abc.abstractmethod
    def __call__(self, registers: list[int], input: Iterator[int]) -> list[int]:
        ...

    @abc.abstractmethod
    def name(self) -> str:
        ...

    @abc.abstractmethod
    def value(self) -> int:
        ...

    @abc.abstractmethod
    def is_input(self) -> bool:
        ...


class BoundParamOperation(Operation):
    def __init__(self, name: str, param_a_pos: int,
                 param_b_pos: int, op: Callable[[int, int], int]):
        self._name = name
        self.param_a_pos = param_a_pos
        self.param_b_pos = param_b_pos
        self.op = op

    def __call__(self, registers: list[int], input: Iterator[int]) -> list[int]:
        registers[self.param_a_pos] = self.op(
            registers[self.param_a_pos], registers[self.param_b_pos])
        return registers

    def name(self) -> str:
        return self._name

    def value(self) -> int:
        raise Exception

    def is_input(self) -> bool:
        return False


class ExactParamOperation(Operation):
    def __init__(self, name: str, param_a_pos: int,
                 param_b_value: int, op: Callable[[int, int], int]):
        self._name = name
        self.param_a_pos = param_a_pos
        self.param_b_value = param_b_value
        self.op = op

    def __call__(self, registers: list[int], input: Iterator[int]) -> list[int]:
        registers[self.param_a_pos] = self.op(registers[self.param_a_pos], self.param_b_value)
        return registers

    def name(self) -> str:
        return self._name

    def value(self) -> int:
        return self.param_b_value

    def is_input(self) -> bool:
        return False


class InputOperation(Operation):
    def __init__(self, var_name: str, var_pos: int):
        self._var_name = var_name
        self._var_pos = var_pos

    def __call__(self, registers: list[int],
                 input: Iterator[int]) -> list[int]:
        num = next(input)
        registers[self._var_pos] = num
        return registers

    def name(self):
        return f"inp {self._var_name}"

    def value(self) -> int:
        raise Exception

    def is_input(self) -> bool:
        return True


class Instruction:
    @staticmethod
    def from_str(line: str) -> Operation:
        match line.split():
            case ["inp", a]:
                return Instruction.inp(a)
            case ["add", a, b]:
                return Instruction.add(a, b)
            case ["mul", a, b]:
                return Instruction.mul(a, b)
            case ["div", a, b]:
                return Instruction.div(a, b)
            case ["mod", a, b]:
                return Instruction.mod(a, b)
            case ["eql", a, b]:
                return Instruction.eql(a, b)
            case _:
                raise Exception

    @staticmethod
    def inp(var_name: str) -> Operation:
        return InputOperation(var_name, "wxyz".find(var_name))

    @staticmethod
    def operation(op_name: str, var_a: str, var_b: str, op: Callable[[int, int], int]) -> Operation:
        vara_pos = "wxyz".find(var_a)
        name = f"{op_name} {var_a} {var_b}"

        match "wxyz".find(var_b):
            case -1:
                return ExactParamOperation(name, vara_pos, int(var_b), op)
            case varb_pos:
                return BoundParamOperation(name, vara_pos, varb_pos, op)

    @staticmethod
    def add(var_a: str, var_b: str):
        return Instruction.operation("add", var_a, var_b, lambda a, b: a + b)

    @staticmethod
    def mul(var_a: str, var_b: str):
        return Instruction.operation("mul", var_a, var_b, lambda a, b: a * b)

    @staticmethod
    def div(var_a: str, var_b: str):
        return Instruction.operation("div", var_a, var_b, lambda a, b: a // b)

    @staticmethod
    def mod(var_a: str, var_b: str):
        return Instruction.operation("mod", var_a, var_b, lambda a, b: a % b)

    @staticmethod
    def eql(var_a: str, var_b: str):
        return Instruction.operation("eql", var_a, var_b, lambda a, b: 1 if a == b else 0)
