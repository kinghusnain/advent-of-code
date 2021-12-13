import 'dart:io';

import 'package:advent_dart/day12.dart';

void main(List<String> args) {
  final input = File('puzzle_input/day12.txt').readAsStringSync();

  var system = CaveSystem.parse(input);
  var paths = system.travelToEndFrom(['start']).toList();
  print(paths.length);

  system = CaveSystem.parse(input);
  paths = system.travelScenicToEndFrom(['start']).toList();
  print(paths.length);
}
