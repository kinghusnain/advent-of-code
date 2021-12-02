int countIncreases(List<int> measurements) {
  if (measurements.isEmpty) return 0;
  int count = 0;
  int prevValue = measurements[0];

  for (final value in measurements) {
    if (value > prevValue) {
      count += 1;
    }
    prevValue = value;
  }
  return count;
}

int countWindowedIncreases(List<int> measurements, int windowSize) {
  List<int> windows = [];

  while (measurements.length >= windowSize) {
    final sum = measurements
        .sublist(0, windowSize)
        .reduce((value, element) => value + element);
    windows.add(sum);
    measurements = measurements.sublist(1);
  }

  return countIncreases(windows);
}
