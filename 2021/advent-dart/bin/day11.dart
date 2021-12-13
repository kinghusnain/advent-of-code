import 'dart:io';

import 'package:advent_dart/day11.dart';

void main(List<String> args) {
  final input = File('puzzle_input/day11.txt').readAsStringSync();
  var sim = OctoSim.parse(input);
  final flashes = List.filled(100, 0)
      .map((_) => sim.step())
      .reduce((value, element) => value + element);
  print(flashes);

  sim = OctoSim.parse(input);
  var step = 1;
  while (sim.step() != sim.numOctopi) {
    step += 1;
  }
  print(step);
}
