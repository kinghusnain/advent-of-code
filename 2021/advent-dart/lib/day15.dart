import 'dart:math';

typedef Pt = Point<int>;

class DangerousCavern {
  final Map<Pt, int> _dangerMap = {};
  late final int _xSize;
  late final int _ySize;
  late final Pt _exit;
  late final int _worstPossibleScore;
  final Map<Pt, int> _leastRiskFrom = {};

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
    _worstPossibleScore = _dangerMap.keys
        .map((pt) => _dangerMap[pt]!)
        .reduce((value, element) => value + element);
  }

  Iterable<Pt> pointsAdjacentTo(Pt pt) sync* {
    if (pt.y > 0) yield Pt(pt.x, pt.y - 1); // Top
    if (pt.x > 0) yield Pt(pt.x - 1, pt.y); // Left
    if (pt.y < _ySize - 1) yield Pt(pt.x, pt.y + 1); // Bottom
    if (pt.x < _xSize - 1) yield Pt(pt.x + 1, pt.y); // Right
  }

  int leastRiskToExit(List<Pt> pathSoFar, int dangerSoFar) {
    final origin = pathSoFar.first;
    final here = pathSoFar.last;

    if (here == _exit) {
      if (dangerSoFar < (_leastRiskFrom[origin] ?? _worstPossibleScore)) {
        _leastRiskFrom[origin] = dangerSoFar;
      }
      return dangerSoFar;
    }
    if (dangerSoFar >= (_leastRiskFrom[origin] ?? _worstPossibleScore)) {
      return _worstPossibleScore;
    }

    final exits =
        pointsAdjacentTo(here).where((pt) => !pathSoFar.contains(pt)).toList();
    exits.sort((p2, p1) => (p1.y + p1.x) - (p2.y + p2.x));
    final scores = exits.map((pt) =>
        leastRiskToExit(pathSoFar + [pt], dangerSoFar + _dangerMap[pt]!));
    return scores.fold(_worstPossibleScore, min);
  }
}
