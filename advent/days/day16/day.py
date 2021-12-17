from __future__ import annotations

import abc
from math import prod
from typing import Generator, Iterator

from advent.common import utils

day_num = 16


def part1(lines: Iterator[str]) -> int:
    bit = Packet.from_str(next(lines))
    return bit.get_version_sum()


def part2(lines: Iterator[str]) -> int:
    bit = Packet.from_str(next(lines))
    return bit.calc_value()


BitConverter = Generator[int, int, None]


@utils.coroutine
def bit_converter(data: Iterator[int]) -> BitConverter:
    bit_count = yield 0
    while True:
        result = 0
        for _ in range(bit_count):
            result = (result << 1) + next(data)
        bit_count = yield result


class Packet(abc.ABC):
    @staticmethod
    def expand(input: str) -> Iterator[int]:
        for char in input:
            digit = int(char, base=16)
            yield int(digit & 0x08 > 0)
            yield int(digit & 0x04 > 0)
            yield int(digit & 0x02 > 0)
            yield int(digit & 0x01 > 0)

    @staticmethod
    def from_str(line: str) -> Packet:
        packet, _ = Packet.create_packet(bit_converter(Packet.expand(line)))
        return packet

    @ staticmethod
    def create_packet(data: BitConverter) -> tuple[Packet, int]:
        version = data.send(3)
        match data.send(3):
            case 4:
                return LiteralPacket.create(data, version)
            case op:
                return OperatorPacket.create(data, version, op)

    @abc.abstractmethod
    def calc_value(self) -> int:
        ...

    @abc.abstractmethod
    def get_version_sum(self) -> int:
        ...


class LiteralPacket(Packet):
    @staticmethod
    def create(data: BitConverter, version: int) -> tuple[Packet, int]:
        consumed = 6
        value = 0
        more = True
        while more:
            more = data.send(1) == 1
            value = (value << 4) + data.send(4)
            consumed += 5
        return LiteralPacket(version, value), consumed

    def __init__(self, version: int, value: int):
        self.version = version
        self.value = value

    def calc_value(self) -> int:
        return self.value

    def get_version_sum(self) -> int:
        return self.version

    def __eq__(self, other: object) -> bool:
        if isinstance(other, LiteralPacket):
            return other.value == self.value and other.version == self.version
        raise NotImplementedError


class OperatorPacket(Packet):
    @staticmethod
    def create(data: BitConverter, version: int, op: int) -> tuple[Packet, int]:
        consumed = 6
        sub_packets: list[Packet] = []
        match data.send(1):
            case 0:
                length = data.send(15)
                consumed += 16 + length
                while length > 0:
                    packet, packet_consumed = Packet.create_packet(data)
                    length -= packet_consumed
                    sub_packets.append(packet)

            case 1:
                count = data.send(11)
                consumed += 12
                for _ in range(count):
                    packet, packet_consumed = Packet.create_packet(data)
                    consumed += packet_consumed
                    sub_packets.append(packet)

            case _:
                raise NotImplementedError

        return OperatorPacket(version, op, sub_packets), consumed

    def __init__(self, version: int, op: int, packets: list[Packet]):
        self.version = version
        self.op = op
        self.packets = packets

    def calc_value(self) -> int:
        match self.op:
            case 0:
                return sum(packet.calc_value() for packet in self.packets)
            case 1:
                return prod(packet.calc_value() for packet in self.packets)
            case 2:
                return min(packet.calc_value() for packet in self.packets)
            case 3:
                return max(packet.calc_value() for packet in self.packets)
            case 5:
                return 1 if self.packets[0].calc_value() > self.packets[1].calc_value() else 0
            case 6:
                return 1 if self.packets[0].calc_value() < self.packets[1].calc_value() else 0
            case 7:
                return 1 if self.packets[0].calc_value() == self.packets[1].calc_value() else 0
            case _:
                raise NotImplementedError

    def get_version_sum(self) -> int:
        return self.version + sum(packet.get_version_sum() for packet in self.packets)

    def __eq__(self, other: object) -> bool:
        try:
            if isinstance(other, OperatorPacket):
                return other.op == self.op and other.version == self.version and all(
                    s == o for s, o in zip(self.packets, other.packets, strict=True))
        except ValueError:
            return False

        raise NotImplementedError
