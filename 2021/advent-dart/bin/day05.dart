import 'dart:io';

import 'package:advent_dart/day05.dart';

void main(List<String> args) {
  final input = File('puzzle_input/day05.txt').readAsLinesSync();

  final segments = input.map((str) => LineSegment.parse(str));
  final dangerRatings =
      segments.where((seg) => seg.isHorizontal || seg.isVertical).dangerRatings;
  dangerRatings.removeWhere((key, value) => value < 2);
  final numDangerPoints = dangerRatings.length;
  print(numDangerPoints);

  final segments2 = input.map((str) => LineSegment.parse(str));
  final dangerRatings2 = segments2.dangerRatings;
  dangerRatings2.removeWhere((key, value) => value < 2);
  final numDangerPoints2 = dangerRatings2.length;
  print(numDangerPoints2);
}
