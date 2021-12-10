import 'dart:io';

import 'package:advent_dart/day01.dart';

void main(List<String> args) {
  final input =
      File('puzzle_input/day01.txt').readAsLinesSync().map(int.parse).toList();
  final part1Soln = countIncreases(input);
  print(part1Soln);
  final part2Soln = countWindowedIncreases(input, 3);
  print(part2Soln);
}
