class HeightMap {
  final List<List<int>> _map;
  late final int _xSize;
  late final int _ySize;

  HeightMap(String mapStr)
      : _map = mapStr
            .trim()
            .split('\n')
            .map((row) => row.split('').map(int.parse).toList(growable: false))
            .toList(growable: false) {
    _ySize = _map.length;
    _xSize = _ySize > 0 ? _map[0].length : 0;
  }

  Iterable<List<int>> adjacentTo(int x, int y) sync* {
    if (y > 0) yield [x, y - 1]; // Top
    if (x > 0) yield [x - 1, y]; // Left
    if (y < _ySize - 1) yield [x, y + 1]; // Bottom
    if (x < _xSize - 1) yield [x + 1, y]; // Right
  }

  bool isLowPoint(int x, int y) {
    final height = _map[y][x];
    for (final adjPt in adjacentTo(x, y)) {
      final adjX = adjPt[0];
      final adjY = adjPt[1];
      if (height >= _map[adjY][adjX]) return false;
    }
    return true;
  }

  Iterable<List<int>> lowPoints() sync* {
    for (var y = 0; y < _ySize; y++) {
      for (var x = 0; x < _xSize; x++) {
        if (isLowPoint(x, y)) yield [x, y];
      }
    }
  }

  int riskOf(int x, int y) => 1 + _map[y][x];

  int get totalRisk => lowPoints()
      .map((p) => riskOf(p[0], p[1]))
      .reduce((value, element) => value + element);
}
