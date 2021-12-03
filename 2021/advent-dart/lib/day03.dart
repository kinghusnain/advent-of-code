int powerConsumption(Iterable<String> report) {
  if (report.isEmpty) return 0;
  final bitTallies = List.filled(report.first.length, 0);

  for (final entry in report) {
    for (var i = 0; i < entry.length; i++) {
      bitTallies[i] += entry[i] == '0' ? -1 : 1;
    }
  }

  var gamma = 0;
  var epsilon = 0;
  for (final tally in bitTallies) {
    final gammaBit = tally > 0 ? 1 : 0;
    gamma = 2 * gamma + gammaBit;
    final epsilonBit = tally < 0 ? 1 : 0;
    epsilon = 2 * epsilon + epsilonBit;
  }

  return gamma * epsilon;
}
