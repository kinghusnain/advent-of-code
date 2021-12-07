import 'package:advent_dart/day06.dart';
import 'package:test/test.dart';

void main() {
  final input = '''3,4,3,1,2'''.split(',').map((e) => int.parse(e));

  test('Part 1 example', () {
    final sim = FishPopulationModel();
    for (var d in input) {
      sim.addFishAtStage(d);
    }
    sim.ffwd(18);
    expect(sim.population, 26);
    sim.ffwd(80 - 18);
    expect(sim.population, 5934);
  });

  test('Part 2 example', () {
    final sim = FishPopulationModel();
    for (var d in input) {
      sim.addFishAtStage(d);
    }
    sim.ffwd(256);
    expect(sim.population, 26984457539);
  });
}
