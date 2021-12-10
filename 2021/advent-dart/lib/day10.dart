const charScores = {
  ')': 3,
  ']': 57,
  '}': 1197,
  '>': 25137,
};

const delimPairs = {'(': ')', '[': ']', '{': '}', '<': '>'};

int errorScore(String chunk) {
  final openChunks = <String>[];
  for (final c in chunk.split('')) {
    switch (c) {
      case '(':
      case '[':
      case '{':
      case '<':
        openChunks.add(c);
        break;
      case ')':
      case ']':
      case '}':
      case '>':
        final oc = openChunks.removeLast();
        if (c != delimPairs[oc]) return charScores[c]!;
        break;
      default:
        throw Exception();
    }
  }
  return 0;
}
