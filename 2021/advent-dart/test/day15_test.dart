import 'package:advent_dart/day15.dart';
import 'package:test/test.dart';

void main() {
  final input = '''1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581''';
  final littleInput = '''116
138
213''';

  test('Part 1 example', () {
    final cavern = DangerousCavern.parse(input);
    int bestScore = cavern.leastRiskToExit([Pt(0, 0)], 0);
    expect(bestScore, 40);
  });

  test('Part 2 example', () {});
}
