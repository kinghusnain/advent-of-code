import 'dart:collection';

import 'dart:math';

class Polymerizer {
  final Map<String, String> _rules = {};
  final Map<String, int> pairCounts = {};
  final Set<String> elements = {};
  late final String _first;
  late final String _last;

  Polymerizer(String template) {
    for (var i = 1; i < template.length; i++) {
      final pair = template.substring(i - 1, i + 1);
      pairCounts[pair] = (pairCounts[pair] ?? 0) + 1;
    }
    _first = template[0];
    _last = template.substring(template.length - 1);
  }

  void addRule(String pair, String element) {
    _rules[pair] = element;
    elements.add(element);
  }

  void applyRules() {
    final counts = Map<String, int>.from(pairCounts);
    for (var pair in counts.keys) {
      final result1 = pair[0] + _rules[pair]!;
      pairCounts[result1] = (pairCounts[result1] ?? 0) + counts[pair]!;
      final result2 = _rules[pair]! + pair[1];
      pairCounts[result2] = (pairCounts[result2] ?? 0) + counts[pair]!;

      pairCounts[pair] = max(0, (pairCounts[pair] ?? 0) - counts[pair]!);
    }
    return;
  }

  SplayTreeMap<String, int> elementCounts() {
    final Map<String, int> counts = {};
    for (var e in elements) {
      final pairs = pairCounts.keys.where((p) => p[0] == e);
      final c = pairs
          .map((p) => pairCounts[p]!)
          .fold(0, (int value, element) => value + element);
      counts[e] = (counts[e] ?? 0) + c;
    }
    counts[_last] = (counts[_last] ?? 0) + 1;
    return SplayTreeMap.from(
        counts, (k1, k2) => (counts[k2] ?? 0) - (counts[k1] ?? 0));
  }
}
