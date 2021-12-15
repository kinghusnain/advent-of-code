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
    var polymer = inputPair[0].trim();
    final polymerizer = Polymerizer(polymer);
    for (final rule in inputPair[1].trim().split('\n')) {
      final rulePair = rule.split('->');
      polymerizer.addRule(rulePair[0].trim(), rulePair[1].trim());
    }
    for (var step = 0; step < 10; step++) {
      polymerizer.applyRules();
    }
    final counts = polymerizer.elementCounts();
    expect((counts[counts.firstKey()] ?? 0) - (counts[counts.lastKey()] ?? 0),
        1588);
  });

  test('Part 2 example', () {
    final inputPair = input.trim().split('\n\n');
    var polymer = inputPair[0].trim();
    final polymerizer = Polymerizer(polymer);
    for (final rule in inputPair[1].trim().split('\n')) {
      final rulePair = rule.split('->');
      polymerizer.addRule(rulePair[0].trim(), rulePair[1].trim());
    }
    for (var step = 0; step < 40; step++) {
      polymerizer.applyRules();
    }
    final counts = polymerizer.elementCounts();
    expect((counts[counts.firstKey()] ?? 0) - (counts[counts.lastKey()] ?? 0),
        2188189693529);
  });
}
