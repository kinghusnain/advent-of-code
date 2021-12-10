const charErrorScores = {
  ')': 3,
  ']': 57,
  '}': 1197,
  '>': 25137,
};

const charCompletionPoints = {
  '(': 1,
  '[': 2,
  '{': 3,
  '<': 4,
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
        if (c != delimPairs[oc]) return charErrorScores[c]!;
        break;
      default:
        throw Exception();
    }
  }
  return 0;
}

int autoCompleteScore(String chunk) {
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
        openChunks.removeLast();
        break;
      default:
        throw Exception();
    }
  }

  var score = 0;
  while (openChunks.isNotEmpty) {
    final c = openChunks.removeLast();
    switch (c) {
      case '(':
      case '[':
      case '{':
      case '<':
        score = 5 * score + charCompletionPoints[c]!;
        break;
      default:
        throw Exception();
    }
  }
  return score;
}
