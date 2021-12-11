import 'dart:math';

typedef Pt = Point<int>;

class HeightMap {
  final Map<Pt, int> _heightMap = {};
  late final int _xSize;
  late final int _ySize;

  HeightMap.parse(String mapString) {
    final map = mapString
        .trim()
        .split('\n')
        .map((row) => row.split('').map(int.parse).toList())
        .toList();
    _xSize = map.isNotEmpty ? map.first.length : 0;
    _ySize = map.length;
    for (var y = 0; y < _ySize; y++) {
      for (var x = 0; x < _xSize; x++) {
        _heightMap[Pt(x, y)] = map[y][x];
      }
    }
  }

  Iterable<Pt> pointsAdjacentTo(Pt pt) sync* {
    if (pt.y > 0) yield Pt(pt.x, pt.y - 1); // Top
    if (pt.x > 0) yield Pt(pt.x - 1, pt.y); // Left
    if (pt.y < _ySize - 1) yield Pt(pt.x, pt.y + 1); // Bottom
    if (pt.x < _xSize - 1) yield Pt(pt.x + 1, pt.y); // Right
  }

  bool isLowPoint(Pt pt) => pointsAdjacentTo(pt)
      .map((adj) => heightAt(pt) < heightAt(adj))
      .reduce((value, element) => value && element);

  Iterable<Pt> lowPoints() => _heightMap.keys.where(isLowPoint);

  int heightAt(Pt pt) {
    final height = _heightMap[pt];
    if (height != null) return height;
    throw Exception();
  }

  int riskOf(Pt pt) => 1 + heightAt(pt);

  int get totalRisk =>
      lowPoints().map(riskOf).reduce((value, element) => value + element);

  Iterable<Pt> pointsUpstreamOf(Pt pt) sync* {
    for (final adjUpstream
        in pointsAdjacentTo(pt).where((adj) => heightAt(adj) > heightAt(pt))) {
      yield adjUpstream;
      for (final farUpstream in pointsUpstreamOf(adjUpstream)) {
        yield farUpstream;
      }
    }
  }

  Set<Pt> basinOf(Pt pt) =>
      {pt, ...pointsUpstreamOf(pt).where((p) => heightAt(p) < 9)};

  Iterable<int> basinSizes() =>
      lowPoints().map(basinOf).map((basin) => basin.length);
}
