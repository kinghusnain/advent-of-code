import 'dart:io';

import 'package:advent_dart/day14.dart';

void main(List<String> args) {
  final input = File('puzzle_input/day14.txt').readAsStringSync();
  final inputPair = input.trim().split('\n\n');
  final polymerizer = Polymerizer();
  var polymer = inputPair[0].trim();
  for (final rule in inputPair[1].trim().split('\n')) {
    final rulePair = rule.split('->');
    polymerizer.addRule(rulePair[0].trim(), rulePair[1].trim());
  }
  for (var _ = 0; _ < 10; _++) {
    polymer = polymerizer.insertInto(polymer);
  }
  var counts = polymer.getElementCounts();
  print((counts[counts.firstKey()] ?? 0) - (counts[counts.lastKey()] ?? 0));
}
