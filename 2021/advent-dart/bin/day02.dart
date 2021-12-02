import 'dart:io';

import 'package:advent_dart/day02.dart';

void main(List<String> args) {
  final input = File('puzzle_input/day02.txt').readAsLinesSync();
  final commands = commandsFromLines(input);
  final position = calculatePosition(commands);
  print(position.horizontal * position.depth);
  final position2 = calculatePositionMk2(commands);
  print(position2.horizontal * position2.depth);
}
