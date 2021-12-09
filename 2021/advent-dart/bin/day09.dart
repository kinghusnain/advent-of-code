import 'dart:io';

import 'package:advent_dart/day09.dart';

void main(List<String> args) {
  final input = File('puzzle_input/day09.txt').readAsStringSync();
  final hmap = HeightMap(input);
  print(hmap.totalRisk);

  final basins = hmap.basinSizes().toList();
  basins.sort((a, b) => b - a);
  final answer = basins.sublist(0, 3).reduce((v, e) => v * e);
  print(answer);
}
