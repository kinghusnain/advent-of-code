import 'package:advent_dart/day14.dart';
import 'package:test/test.dart';

void main() {
  final input = '''NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C''';

  test('Part 1 example', () {
    final inputPair = input.trim().split('\n\n');
    final polymerizer = Polymerizer();
    var polymer = inputPair[0].trim();
    for (final rule in inputPair[1].trim().split('\n')) {
      final rulePair = rule.split('->');
      polymerizer.addRule(rulePair[0].trim(), rulePair[1].trim());
    }
    for (var _ = 0; _ < 10; _++) {
      polymer = polymerizer.insertInto(polymer);
    }
    final counts = polymer.getElementCounts();
    expect((counts[counts.firstKey()] ?? 0) - (counts[counts.lastKey()] ?? 0),
        1588);
  });
}
