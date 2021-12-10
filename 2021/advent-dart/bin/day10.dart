import 'dart:io';

import 'package:advent_dart/day10.dart';

void main(List<String> args) {
  final input = File('puzzle_input/day10.txt').readAsLinesSync();
  final totalScore =
      input.map(errorScore).reduce((value, element) => value + element);
  print(totalScore);
}
