import 'dart:io';

import 'package:advent_dart/day15.dart';

void main(List<String> args) {
  final input = File('puzzle_input/day15.txt').readAsStringSync();
  final cavern = DangerousCavern.parse(input);
  final path = cavern.shortestPathToExit();
  final cost = cavern.costOfPath(path);
  print(cost);
}
