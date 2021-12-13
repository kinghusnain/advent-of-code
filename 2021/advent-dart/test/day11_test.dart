import 'package:advent_dart/day11.dart';
import 'package:test/test.dart';

void main() {
  final input = '''5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526
''';

  test('Part 1 example', () {
    final sim = OctoSim.parse(input);
    final flashes = List.filled(100, 0)
        .map((_) => sim.step())
        .reduce((value, element) => value + element);
    expect(flashes, 1656);
  });

  test('Part 2 example', () {
    final sim = OctoSim.parse(input);
    var step = 1;
    while (sim.step() != sim.numOctopi) {
      step += 1;
    }
    expect(step, 195);
  });
}
