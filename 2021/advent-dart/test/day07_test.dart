import 'package:advent_dart/day07.dart';
import 'package:test/test.dart';

void main() {
  final input = '''16,1,2,0,4,2,7,1,2,14'''.split(',').map((e) => int.parse(e));

  test('Part 1 example', () {
    final leastCost = leastCostToAlign(input.toList());
    expect(leastCost, 37);
  });

  test('Part 2 example', () {
    final leastCost = leastCostToAlignV2(input.toList());
    expect(leastCost, 168);
  });
}
