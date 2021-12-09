import 'dart:io';

import 'package:advent_dart/day09.dart';

void main(List<String> args) {
  final input = File('puzzle_input/day09.txt').readAsStringSync();
  final hmap = HeightMap(input);
  print(hmap.totalRisk);
}
