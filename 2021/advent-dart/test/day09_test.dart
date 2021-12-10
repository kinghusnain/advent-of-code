import 'package:advent_dart/day09.dart';
import 'package:test/test.dart';

void main() {
  final input = '''2199943210
3987894921
9856789892
8767896789
9899965678''';

  test('Part 1 example', () {
    final hmap = HeightMap.parse(input);
    expect(hmap.totalRisk, 15);
  });

  test('Part 2 example', () {
    final hmap = HeightMap.parse(input);
    expect(hmap.basinOf(Pt(1, 0)).length, 3);
    expect(hmap.basinOf(Pt(9, 0)).length, 9);
    expect(hmap.basinOf(Pt(2, 2)).length, 14);
    expect(hmap.basinOf(Pt(6, 4)).length, 9);

    final basins = hmap.basinSizes().toList();
    basins.sort((a, b) => b - a);
    final answer = basins.sublist(0, 3).reduce((v, e) => v * e);
    expect(answer, 1134);
  });
}
