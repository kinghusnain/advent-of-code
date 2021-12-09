import 'package:advent_dart/day09.dart';
import 'package:test/test.dart';

void main() {
  final input = '''2199943210
3987894921
9856789892
8767896789
9899965678''';

  test('Part 1 example', () {
    final hmap = HeightMap(input);
    expect(hmap.totalRisk, 15);
  });
}
