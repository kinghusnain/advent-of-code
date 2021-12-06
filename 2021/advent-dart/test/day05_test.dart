import 'package:advent_dart/day05.dart';
import 'package:test/test.dart';

void main() {
  final input = '''0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2'''
      .split('\n');

  test('Part 1 example', () {
    final segments = input.map((str) => LineSegment.parse(str));
    final dangerRatings = segments
        .where((seg) => seg.isHorizontal || seg.isVertical)
        .dangerRatings;
    dangerRatings.removeWhere((key, value) => value < 2);
    final numDangerPoints = dangerRatings.length;
    expect(numDangerPoints, 5);
  });

  test('Part 2 example', () {
    final segments = input.map((str) => LineSegment.parse(str));
    final dangerRatings = segments.dangerRatings;
    dangerRatings.removeWhere((key, value) => value < 2);
    final numDangerPoints = dangerRatings.length;
    expect(numDangerPoints, 12);
  });
}
