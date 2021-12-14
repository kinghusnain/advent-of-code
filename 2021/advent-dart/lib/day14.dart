import 'dart:collection';

typedef Polymer = String;

extension PolymerMethods on Polymer {
  SplayTreeMap<String, int> getElementCounts() {
    final counts = <String, int>{};
    for (final c in split('')) {
      counts[c] = (counts[c] ?? 0) + 1;
    }
    return SplayTreeMap.from(
        counts, (k1, k2) => (counts[k2] ?? 0) - (counts[k1] ?? 0));
  }
}

class Polymerizer {
  final Map<String, String> _rules = {};

  void addRule(String pair, String element) {
    _rules[pair] = element;
  }

  String lookup(String pair) {
    final element = _rules[pair];
    if (element != null) return element;
    throw Exception();
  }

  Iterable<String> _insertInto(Polymer polymer) sync* {
    if (polymer.length < 2) {
      yield polymer;
    } else {
      for (var i = 1; i < polymer.length; i++) {
        yield polymer[i - 1];
        yield lookup(polymer.substring(i - 1, i + 1));
      }
      yield polymer[polymer.length - 1];
    }
  }

  Polymer insertInto(Polymer polymer) => _insertInto(polymer).join('');
}
