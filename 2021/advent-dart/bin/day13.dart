import 'dart:io';

import 'package:advent_dart/day13.dart';

void main(List<String> args) {
  final input = File('puzzle_input/day13.txt').readAsStringSync();
  final inputPair = input.trim().split('\n\n');
  final dotsInput = inputPair[0].trim();
  final origami = TransparentOrigami.parse(dotsInput);
  final foldInput = inputPair[1].trim();

  final instr = foldInput.split('\n').first;
  origami.fold(instr);
  print(origami.dots.length);

  for (final instr in foldInput.split('\n').skip(1)) {
    origami.fold(instr);
  }
  print(origami);
}
