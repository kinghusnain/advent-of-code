import 'dart:math';

typedef Pt = Point<int>;

class DangerousCavern {
  final Map<Pt, int> _dangerMap = {};
  late final int _xSize;
  late final int _ySize;
  late final Pt _exit;

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

  List<Pt> shortestPathToExit() => dijkstra(Pt(0, 0), _exit);

  List<Pt> dijkstra(Pt start, Pt goal) {
    final openSet = _dangerMap.keys.toList();
    final Map<Pt, Pt> cameFrom = {};

    final distancesTo = Map.fromIterables(
        _dangerMap.keys, List.filled(_dangerMap.length, _xSize * _ySize * 9));
    distancesTo[start] = 0;

    while (openSet.isNotEmpty) {
      openSet.sort((pt1, pt2) => distancesTo[pt1]! - distancesTo[pt2]!);
      final u = openSet.first;
      openSet.removeWhere((pt) => pt == u);

      if (u == goal) return reconstructPath(cameFrom, u);

      for (var v in pointsAdjacentTo(u)) {
        final alt = distancesTo[u]! + _dangerMap[v]!;
        if (alt < distancesTo[v]!) {
          distancesTo[v] = alt;
          cameFrom[v] = u;
        }
      }
    }

    throw Exception();
  }

  List<Pt> reconstructPath(Map<Pt, Pt> cameFrom, Pt current) {
    final totalPath = [current];
    while (cameFrom.containsKey(current)) {
      current = cameFrom[current]!;
      totalPath.insert(0, current);
    }
    return totalPath;
  }

  int costOfPath(List<Pt> path) => path
      .sublist(1)
      .map((pt) => _dangerMap[pt]!)
      .fold(0, (value, element) => value + element);
}
