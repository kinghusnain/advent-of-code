import 'dart:io';

import 'package:advent_dart/day15.dart';

void main(List<String> args) {
  final input = File('puzzle_input/day15.txt').readAsStringSync();

  var cavern = DangerousCavern.parse(input);
  var path = cavern.shortestPathToExit();
  var cost = cavern.costOfPath(path);
  print(cost);

  cavern = BigDangerousCavern.parse(input);
  path = cavern.shortestPathToExit();
  cost = cavern.costOfPath(path);
  print(cost);
}
