import 'dart:io';

import 'package:advent_dart/day16.dart';

void main(List<String> args) {
  final input = File('puzzle_input/day16.txt').readAsStringSync().trim();
  final packet = Packet.parse(input.hexToBin());
  final versionSum = packet
      .decendPacketTree()
      .map((p) => p.version)
      .reduce((value, element) => value + element);
  print(versionSum);
}
