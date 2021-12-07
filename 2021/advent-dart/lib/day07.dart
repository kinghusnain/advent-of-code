import 'dart:math';

typedef CrabPositions = List<int>;

int leastCostToAlign(CrabPositions positions) {
  var lowest = positions.length * positions.length;

  for (var alignPos = 0; alignPos < positions.length; alignPos++) {
    var total = 0;
    for (final pos in positions) {
      total += (alignPos - pos).abs();
      if (total > lowest) break;
    }
    lowest = min(lowest, total);
  }

  return lowest;
}

int leastCostToAlignV2(CrabPositions positions) {
  var lowest = double.maxFinite.toInt();

  for (var alignPos = 0; alignPos < positions.length; alignPos++) {
    var total = 0;
    for (final pos in positions) {
      final distance = (alignPos - pos).abs();
      final cost = List.generate(distance, (i) => i + 1)
          .fold(0, (int value, element) => value + element);
      total += cost;
      if (total > lowest) break;
    }
    lowest = min(lowest, total);
  }

  return lowest;
}
