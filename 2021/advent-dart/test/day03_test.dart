import 'package:advent_dart/day03.dart';
import 'package:test/test.dart';

void main() {
  final input = '''00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010'''
      .split('\n');

  test('Part 1 example', () {
    expect(powerConsumption(input), 198);
  });

  test('Part 2 example', () {
    expect(lifeSupportRating(input), 230);
  });
}
