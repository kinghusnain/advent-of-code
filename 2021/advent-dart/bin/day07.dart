import 'dart:io';

import 'package:advent_dart/day07.dart';

void main(List<String> args) {
  final input = File('puzzle_input/day07.txt')
      .readAsStringSync()
      .split(',')
      .map((e) => int.parse(e))
      .toList();
  final pt1 = leastCostToAlign(input);
  print(pt1);
  final pt2 = leastCostToAlignV2(input);
  print(pt2);
}
