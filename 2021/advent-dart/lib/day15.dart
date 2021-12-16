import 'dart:math';

import 'package:collection/collection.dart';

typedef Pt = Point<int>;

class DangerousCavern {
  final Map<Pt, int> _dangerMap = {};
  late final int _xSize;
  late final int _ySize;
  late final Pt _exit;

  DangerousCavern();
  DangerousCavern.parse(String mapString) {
    final map = mapString
        .trim()
        .split('\n')
        .map((row) => row.split('').map(int.parse).toList())
        .toList();
    _xSize = map.isNotEmpty ? map.first.length : 0;
    _ySize = map.length;
    _exit = Pt(_xSize - 1, _ySize - 1);
    for (var y = 0; y < _ySize; y++) {
      for (var x = 0; x < _xSize; x++) {
        _dangerMap[Pt(x, y)] = map[y][x];
      }
    }
  }

  Iterable<Pt> pointsAdjacentTo(Pt pt) sync* {
    if (pt.y > 0) yield Pt(pt.x, pt.y - 1); // Top
    if (pt.x > 0) yield Pt(pt.x - 1, pt.y); // Left
    if (pt.y < _ySize - 1) yield Pt(pt.x, pt.y + 1); // Bottom
    if (pt.x < _xSize - 1) yield Pt(pt.x + 1, pt.y); // Right
  }

  int leastCostToExit() => dijkstra(Pt(0, 0), _exit);

  int dijkstra(Pt start, Pt goal) {
    final distancesTo = Map.fromIterables(
        _dangerMap.keys, List.filled(_dangerMap.length, _xSize * _ySize * 9));
    distancesTo[start] = 0;

    final openSet =
        HeapPriorityQueue<Pt>((a, b) => distancesTo[a]! - distancesTo[b]!);
    openSet.add(start);

    while (openSet.isNotEmpty) {
      final u = openSet.removeFirst();
      if (u == goal) return distancesTo[u]!;

      for (var v in pointsAdjacentTo(u)) {
        final alt = distancesTo[u]! + _dangerMap[v]!;
        if (alt < distancesTo[v]!) {
          distancesTo[v] = alt;
          openSet.add(v);
        }
      }
    }

    throw Exception();
  }
}

class BigDangerousCavern extends DangerousCavern {
  BigDangerousCavern.parse(String mapString) : super() {
    final map = mapString
        .trim()
        .split('\n')
        .map((row) => row.split('').map(int.parse).toList())
        .toList();
    final baseXSize = map.isNotEmpty ? map.first.length : 0;
    final baseYSize = map.length;
    for (var y = 0; y < baseYSize; y++) {
      for (var x = 0; x < baseXSize; x++) {
        for (var yn = 0; yn < 5; yn++) {
          for (var xn = 0; xn < 5; xn++) {
            var val = (map[y][x] + xn + yn);
            while (val > 9) val = (val % 10) + 1;
            _dangerMap[Pt(x + xn * baseXSize, y + yn * baseYSize)] = val;
          }
        }
      }
    }
    _xSize = 5 * baseXSize;
    _ySize = 5 * baseYSize;
    _exit = Pt(_xSize - 1, _ySize - 1);
  }
}
