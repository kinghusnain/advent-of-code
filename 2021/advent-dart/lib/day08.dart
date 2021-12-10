class SevenSegmentDisplaySolver {
  // 0: 6 segments, not 9, superset of 1.
  // 1: 2 segments.
  // 2: 5 segments, not 3, not 5.
  // 3: 5 segments, superset of 1.
  // 4: 4 segments.
  // 5: 5 segments, subset of 6.
  // 6: 6 segments, not 9, not 0.
  // 7: 3 segments.
  // 8: 7 segments.
  // 9: 6 segments, superset of 4.
  final List<String?> _ssdRepresentations = List.filled(10, null);
  final Map<String, int> decoder = {};

  SevenSegmentDisplaySolver(Set<String> uniquePatterns) {
    _ssdRepresentations[1] = uniquePatterns
        .where((pattern) => pattern.length == 2)
        .single
        .alphabetized();
    _ssdRepresentations[4] = uniquePatterns
        .where((pattern) => pattern.length == 4)
        .single
        .alphabetized();
    _ssdRepresentations[7] = uniquePatterns
        .where((pattern) => pattern.length == 3)
        .single
        .alphabetized();
    _ssdRepresentations[8] = uniquePatterns
        .where((pattern) => pattern.length == 7)
        .single
        .alphabetized();
    _ssdRepresentations[9] = uniquePatterns
        .where((pattern) => pattern.length == 6)
        .map((e) => e.alphabetized())
        .where((pattern) =>
            pattern.toSet().containsAll(_ssdRepresentations[4]!.toSet()))
        .single;
    _ssdRepresentations[0] = uniquePatterns
        .where((pattern) => pattern.length == 6)
        .map((e) => e.alphabetized())
        .where((pattern) => pattern != _ssdRepresentations[9])
        .where((pattern) =>
            pattern.toSet().containsAll(_ssdRepresentations[1]!.toSet()))
        .single;
    _ssdRepresentations[6] = uniquePatterns
        .where((pattern) => pattern.length == 6)
        .map((e) => e.alphabetized())
        .where((pattern) => pattern != _ssdRepresentations[9])
        .where((pattern) => pattern != _ssdRepresentations[0])
        .single;
    _ssdRepresentations[3] = uniquePatterns
        .where((pattern) => pattern.length == 5)
        .map((e) => e.alphabetized())
        .where((pattern) =>
            pattern.toSet().containsAll(_ssdRepresentations[1]!.toSet()))
        .single;
    _ssdRepresentations[5] = uniquePatterns
        .where((pattern) => pattern.length == 5)
        .map((e) => e.alphabetized())
        .where((pattern) =>
            _ssdRepresentations[6]!.toSet().containsAll(pattern.toSet()))
        .single;
    _ssdRepresentations[2] = uniquePatterns
        .where((pattern) => pattern.length == 5)
        .map((e) => e.alphabetized())
        .where((pattern) => pattern != _ssdRepresentations[5])
        .where((pattern) => pattern != _ssdRepresentations[3])
        .single;

    for (var i = 0; i < 10; i++) {
      decoder[_ssdRepresentations[i]!] = i;
    }
  }
}

Iterable<String> oneFourSevenEight(Iterable<String> uniquePatterns) =>
    uniquePatterns
        .where((pattern) => [2, 4, 3, 7].contains(pattern.length))
        .map((pattern) => pattern.alphabetized());

class LogEntry {
  late Set<String> uniquePatterns;
  late List<String> outputs;

  LogEntry(this.uniquePatterns, this.outputs);
  LogEntry.parse(String string) {
    final sections = string.split(' | ');
    uniquePatterns = sections[0].split(' ').toSet();
    outputs = sections[1].split(' ');
  }

  String decode() {
    final solver = SevenSegmentDisplaySolver(uniquePatterns);
    return outputs.map((e) => solver.decoder[e.alphabetized()]).join();
  }
}

extension StringUtils on String {
  String alphabetized() {
    final chars = split('');
    chars.sort();
    return chars.reduce((value, element) => value + element);
  }

  Set<String> toSet() => Set.from(split(''));
}
