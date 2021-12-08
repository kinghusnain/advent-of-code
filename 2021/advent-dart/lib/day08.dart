class SevenSegmentDisplaySolver {
  // 0: 6 segments, not 9, contains 1
  // 1: 2 segments
  // 2: 5 segments,
  // 3: 5 segments, contains 1
  // 4: 4 segments
  // 5: 5 segments,
  // 6: 6 segments, not 9, not 0
  // 7: 3 segments
  // 8: 7 segments
  // 9: 6 segments, contains 4
  final List<String?> ssdRepresentations = List.filled(10, null);
  final Map<String, int> decoder = {};

  SevenSegmentDisplaySolver(List<String> uniquePatterns) {
    ssdRepresentations[1] = uniquePatterns
        .where((pattern) => pattern.length == 2)
        .firstAndOnly()
        .alphabetized();
    ssdRepresentations[4] = uniquePatterns
        .where((pattern) => pattern.length == 4)
        .firstAndOnly()
        .alphabetized();
    ssdRepresentations[7] = uniquePatterns
        .where((pattern) => pattern.length == 3)
        .firstAndOnly()
        .alphabetized();
    ssdRepresentations[8] = uniquePatterns
        .where((pattern) => pattern.length == 7)
        .firstAndOnly()
        .alphabetized();
    ssdRepresentations[9] = uniquePatterns
        .where((pattern) => pattern.length == 6)
        .map((e) => e.alphabetized())
        .where((pattern) =>
            pattern.toSet().containsAll(ssdRepresentations[4]!.toSet()))
        .firstAndOnly();
    ssdRepresentations[0] = uniquePatterns
        .where((pattern) => pattern.length == 6)
        .map((e) => e.alphabetized())
        .where((pattern) => pattern != ssdRepresentations[9])
        .where((pattern) =>
            pattern.toSet().containsAll(ssdRepresentations[1]!.toSet()))
        .firstAndOnly();
    ssdRepresentations[6] = uniquePatterns
        .where((pattern) => pattern.length == 6)
        .map((e) => e.alphabetized())
        .where((pattern) => pattern != ssdRepresentations[9])
        .where((pattern) => pattern != ssdRepresentations[0])
        .firstAndOnly();
    ssdRepresentations[3] = uniquePatterns
        .where((pattern) => pattern.length == 5)
        .map((e) => e.alphabetized())
        .where((pattern) =>
            pattern.toSet().containsAll(ssdRepresentations[1]!.toSet()))
        .firstAndOnly();
    ssdRepresentations[5] = uniquePatterns
        .where((pattern) => pattern.length == 5)
        .map((e) => e.alphabetized())
        .where((pattern) =>
            ssdRepresentations[6]!.toSet().containsAll(pattern.toSet()))
        .firstAndOnly();
    ssdRepresentations[2] = uniquePatterns
        .where((pattern) => pattern.length == 5)
        .map((e) => e.alphabetized())
        .where((pattern) => pattern != ssdRepresentations[5])
        .where((pattern) => pattern != ssdRepresentations[3])
        .firstAndOnly();

    for (var i = 0; i < 10; i++) {
      decoder[ssdRepresentations[i]!] = i;
    }
  }
}

Iterable<String> oneFourSevenEight(Iterable<String> uniquePatterns) =>
    uniquePatterns
        .where((pattern) => [2, 4, 3, 7].contains(pattern.length))
        .map((pattern) => pattern.alphabetized());

class LogEntry {
  late List<String> uniquePatterns;
  late List<String> outputs;

  LogEntry(this.uniquePatterns, this.outputs);
  LogEntry.parse(String string) {
    final sections = string.split(' | ');
    uniquePatterns = sections[0].split(' ');
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

extension IterUtils<T> on Iterable<T> {
  T firstAndOnly() {
    if (length != 1) throw Exception();
    return first;
  }
}
