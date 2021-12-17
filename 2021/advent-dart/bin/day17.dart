import 'package:advent_dart/day17.dart';

void main(List<String> args) {
  // target area: x=135..155, y=-102..-78
  final target = TargetArea(135, 155, -102, -78);
  final apex = bestApex(target);
  print(apex);

  final goodVelocities = findGoodVelocities(target).toSet();
  print(goodVelocities.length);
}
