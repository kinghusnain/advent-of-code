import 'dart:io';

import 'package:advent_dart/day03.dart';

void main(List<String> args) {
  final input = File('puzzle_input/day03.txt').readAsLinesSync();
  final pt1Soln = powerConsumption(input);
  print(pt1Soln);
}
