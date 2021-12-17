import 'dart:io';

import 'package:advent_dart/day16.dart';
import 'package:test/test.dart';

void main() {
  test('Hex string to bin string', () {
    expect('0'.hexToBin(), '0000');
    expect('2'.hexToBin(), '0010');
    expect('A'.hexToBin(), '1010');
    expect('AB'.hexToBin(), '10101011');
    expect('D2FE28'.hexToBin(), '110100101111111000101000');
  });

  test('Literal packets', () {
    expect(LiteralPacket.parse('D2FE28'.hexToBin()).value, 2021);
  });

  test('Operator packets', () {
    var packet = OperatorPacket.parse(
      '38006F45291200'.hexToBin(),
      operatorFunction: (_) => throw UnimplementedError(),
    );
    expect(packet.subPackets.length, 2);
    expect(packet.subPackets[0], isA<LiteralPacket>());
    expect((packet.subPackets[0] as LiteralPacket).value, 10);
    expect(packet.subPackets[1], isA<LiteralPacket>());
    expect((packet.subPackets[1] as LiteralPacket).value, 20);

    packet = OperatorPacket.parse(
      'EE00D40C823060'.hexToBin(),
      operatorFunction: (_) => throw UnimplementedError(),
    );
    expect(packet.subPackets.length, 3);
    expect(packet.subPackets[0], isA<LiteralPacket>());
    expect((packet.subPackets[0] as LiteralPacket).value, 1);
    expect(packet.subPackets[1], isA<LiteralPacket>());
    expect((packet.subPackets[1] as LiteralPacket).value, 2);
    expect(packet.subPackets[2], isA<LiteralPacket>());
    expect((packet.subPackets[2] as LiteralPacket).value, 3);
  });

  test('Part 1 examples', () {
    var packet = Packet.parse('8A004A801A8002F478'.hexToBin());
    var versionSum = packet
        .decendPacketTree()
        .map((p) => p.version)
        .reduce((value, element) => value + element);
    expect(versionSum, 16);

    packet = Packet.parse('620080001611562C8802118E34'.hexToBin());
    versionSum = packet
        .decendPacketTree()
        .map((p) => p.version)
        .reduce((value, element) => value + element);
    expect(versionSum, 12);

    packet = Packet.parse('C0015000016115A2E0802F182340'.hexToBin());
    versionSum = packet
        .decendPacketTree()
        .map((p) => p.version)
        .reduce((value, element) => value + element);
    expect(versionSum, 23);

    packet = Packet.parse('A0016C880162017C3686B18A3D4780'.hexToBin());
    versionSum = packet
        .decendPacketTree()
        .map((p) => p.version)
        .reduce((value, element) => value + element);
    expect(versionSum, 31);
  });

  test('Part 2 examples', () {
    expect(Packet.parse('C200B40A82'.hexToBin()).value, 3);
    expect(Packet.parse('04005AC33890'.hexToBin()).value, 54);
    expect(Packet.parse('880086C3E88112'.hexToBin()).value, 7);
    expect(Packet.parse('CE00C43D881120'.hexToBin()).value, 9);
    expect(Packet.parse('D8005AC2A8F0'.hexToBin()).value, 1);
    expect(Packet.parse('F600BC2D8F'.hexToBin()).value, 0);
    expect(Packet.parse('9C005AC2F8F0'.hexToBin()).value, 0);
    expect(Packet.parse('9C0141080250320F1802104A08'.hexToBin()).value, 1);
  });

  test('Puzzle solutions', () {
    final input = File('puzzle_input/day16.txt').readAsStringSync().trim();
    final packet = Packet.parse(input.hexToBin());
    final versionSum = packet
        .decendPacketTree()
        .map((p) => p.version)
        .reduce((value, element) => value + element);
    expect(versionSum, 929);
    expect(packet.value, 911945136934);
  });
}
