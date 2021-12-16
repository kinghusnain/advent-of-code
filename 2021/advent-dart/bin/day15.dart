import 'dart:io';

import 'package:advent_dart/day15.dart';

void main(List<String> args) {
  final input = File('puzzle_input/day15.txt').readAsStringSync();

  var cavern = DangerousCavern.parse(input);
  var cost = cavern.leastCostToExit();
  print(cost);

  cavern = BigDangerousCavern.parse(input);
  cost = cavern.leastCostToExit();
  print(cost);
}
