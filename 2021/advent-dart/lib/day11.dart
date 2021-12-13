import 'dart:math';

typedef Pt = Point<int>;

class OctoSim {
  final Map<Pt, int> _energyMap = {};
  late final int _xSize;
  late final int _ySize;
  int get numOctopi => _xSize * _ySize;

  OctoSim.parse(String mapString) {
    final map = mapString
        .trim()
        .split('\n')
        .map((row) => row.split('').map(int.parse).toList())
        .toList();
    _xSize = map.isNotEmpty ? map.first.length : 0;
    _ySize = map.length;
    for (var y = 0; y < _ySize; y++) {
      for (var x = 0; x < _xSize; x++) {
        _energyMap[Pt(x, y)] = map[y][x];
      }
    }
  }

  int step() {
    for (final pt in _energyMap.keys) {
      _energyMap[pt] = _energyMap[pt]! + 1;
    }

    final Set<Pt> flashed = {};
    var done = false;
    while (!done) {
      done = true;
      for (final pt in _energyMap.keys
          .where((pt) => _energyMap[pt]! > 9 && !flashed.contains(pt))) {
        flashed.add(pt);
        done = false;
        for (var adj in pointsAdjacentTo(pt)) {
          _energyMap[adj] = _energyMap[adj]! + 1;
        }
      }
    }
    for (final pt in _energyMap.keys.where((pt) => _energyMap[pt]! > 9)) {
      _energyMap[pt] = 0;
    }
    return flashed.length;
  }

  Iterable<Pt> pointsAdjacentTo(Pt pt) sync* {
    if (pt.y > 0) yield Pt(pt.x, pt.y - 1); // Top
    if (pt.x > 0) yield Pt(pt.x - 1, pt.y); // Left
    if (pt.y < _ySize - 1) yield Pt(pt.x, pt.y + 1); // Bottom
    if (pt.x < _xSize - 1) yield Pt(pt.x + 1, pt.y); // Right
    if (pt.y > 0 && pt.x > 0) yield Pt(pt.x - 1, pt.y - 1); // tl
    if (pt.y > 0 && pt.x < _xSize - 1) yield Pt(pt.x + 1, pt.y - 1); // tr
    if (pt.y < _ySize - 1 && pt.x > 0) yield Pt(pt.x - 1, pt.y + 1); // bl
    if (pt.y < _ySize - 1 && pt.x < _xSize - 1)
      yield Pt(pt.x + 1, pt.y + 1); // br
  }
}
