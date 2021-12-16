from advent.common import utils
from . day import Packet, LiteralPacket, OperatorPacket, part1, part2


def test_expand():
    input = "D2FE28"
    expected = "110100101111111000101000"
    result = "".join(str(d) for d in Packet.expand(input))
    assert result == expected


def test_read():
    input = "D2FE28"
    expected = LiteralPacket(6, 2021)
    result = Packet.from_str(input)
    assert result == expected


def test_operator1():
    input = "38006F45291200"
    expected = OperatorPacket(1, 6, [LiteralPacket(6, 10), LiteralPacket(2, 20)])
    result = Packet.from_str(input)
    assert result == expected


def test_operator2():
    input = "EE00D40C823060"
    expected = OperatorPacket(7, 3, [LiteralPacket(2, 1), LiteralPacket(4, 2), LiteralPacket(1, 3)])
    result = Packet.from_str(input)
    assert result == expected


def test_version1():
    input = "8A004A801A8002F478"
    expected = 16
    result = Packet.from_str(input).get_version_sum()
    assert result == expected


def test_version2():
    input = "620080001611562C8802118E34"
    expected = 12
    result = Packet.from_str(input).get_version_sum()
    assert result == expected


def test_version3():
    input = "C0015000016115A2E0802F182340"
    expected = 23
    result = Packet.from_str(input).get_version_sum()
    assert result == expected


def test_version4():
    input = "A0016C880162017C3686B18A3D4780"
    expected = 31
    result = Packet.from_str(input).get_version_sum()
    assert result == expected


def test_op_value1():
    input = "C200B40A82"
    expected = 3
    result = Packet.from_str(input).calc_value()
    assert result == expected


def test_op_value2():
    input = "04005AC33890"
    expected = 54
    result = Packet.from_str(input).calc_value()
    assert result == expected


def test_op_value3():
    input = "880086C3E88112"
    expected = 7
    result = Packet.from_str(input).calc_value()
    assert result == expected


def test_part1():
    input = utils.read_data(16, "test01.txt")
    expected = 23
    result = part1(input)
    assert result == expected


def test_part2():
    input = utils.read_data(16, "test02.txt")
    expected = 1
    result = part2(input)
    assert result == expected
