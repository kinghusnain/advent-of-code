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
}

extension StringUtils on String {
  String alphabetized() {
    final chars = split('');
    chars.sort();
    return chars.reduce((value, element) => value + element);
  }
}
