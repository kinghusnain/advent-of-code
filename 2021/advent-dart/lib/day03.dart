int powerConsumption(Iterable<String> report) {
  if (report.isEmpty) return 0;
  final bitTallies = tallyBits(report);

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

int lifeSupportRating(Iterable<String> report) {
  if (report.isEmpty) return 0;

  final o2Data = report.toList();
  var i = 0;
  while (o2Data.length > 1) {
    final bitTallies = tallyBits(o2Data);
    final bitCriterion = bitTallies[i] < 0 ? '0' : '1';
    o2Data.removeWhere((entry) => entry[i] != bitCriterion);
    i += 1;
  }
  final o2Rating = int.parse(o2Data.first, radix: 2);

  final co2Data = report.toList();
  i = 0;
  while (co2Data.length > 1) {
    final bitTallies = tallyBits(co2Data);
    final bitCriterion = bitTallies[i] < 0 ? '1' : '0';
    co2Data.removeWhere((entry) => entry[i] != bitCriterion);
    i += 1;
  }
  final co2Rating = int.parse(co2Data.first, radix: 2);

  return o2Rating * co2Rating;
}

List<int> tallyBits(Iterable<String> report) {
  final bitTallies = List.filled(report.first.length, 0);

  for (final entry in report) {
    for (var i = 0; i < entry.length; i++) {
      bitTallies[i] += entry[i] == '0' ? -1 : 1;
    }
  }

  return bitTallies;
}
