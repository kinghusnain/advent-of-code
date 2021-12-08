import 'dart:io';

import 'package:advent_dart/day08.dart';

void main(List<String> args) {
  final input = File('puzzle_input/day08.txt')
      .readAsLinesSync()
      .map((entry) => LogEntry.parse(entry));
  final num1478s = input.map((e) {
    final patterns = oneFourSevenEight(e.uniquePatterns);
    return e.outputs
        .where((out) => patterns.contains(out.alphabetized()))
        .length;
  }).reduce((value, element) => value + element);
  print(num1478s);
}
