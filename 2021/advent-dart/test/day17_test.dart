import 'package:advent_dart/day17.dart';
import 'package:test/test.dart';

void main() {
  test('Part 1 example', () {
    final target = TargetArea(20, 30, -10, -5);
    final apex = bestApex(target);
    expect(apex, 45);
  });

  test('Part 2 example', () {
    final target = TargetArea(20, 30, -10, -5);
    final goodVelocities = findGoodVelocities(target).toSet();
    expect(goodVelocities.length, 112);
  });

  test('Puzzle solutions', () {
    // target area: x=135..155, y=-102..-78
    final target = TargetArea(135, 155, -102, -78);
    final apex = bestApex(target);
    expect(apex, 5151);

    final goodVelocities = findGoodVelocities(target).toSet();
    expect(goodVelocities.length, 968);
  });
}
