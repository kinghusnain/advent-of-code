import 'dart:io';

import 'package:advent_dart/day06.dart';

void main(List<String> args) {
  final input = File('puzzle_input/day06.txt')
      .readAsStringSync()
      .split(',')
      .map((e) => int.parse(e));
  var sim = FishPopulationModel();
  for (var d in input) {
    sim.addFishAtStage(d);
  }
  sim.ffwd(80);
  print(sim.population);

  sim = FishPopulationModel();
  for (var d in input) {
    sim.addFishAtStage(d);
  }
  sim.ffwd(256);
  print(sim.population);
}
