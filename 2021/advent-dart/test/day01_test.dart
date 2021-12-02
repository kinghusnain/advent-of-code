import 'package:advent_dart/day01.dart';
import 'package:test/test.dart';

void main() {
  final input = [
    199,
    200,
    208,
    210,
    200,
    207,
    240,
    269,
    260,
    263,
  ];
  test('Part 1 example', () {
    expect(countIncreases(input), 7);
  });
  test('Part 2 example', () {
    expect(countWindowedIncreases(input, 3), 5);
  });
}
