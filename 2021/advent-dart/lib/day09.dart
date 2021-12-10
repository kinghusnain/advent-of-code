import 'dart:math';

typedef Pt = Point<int>;

class HeightMap {
  final List<List<int>> _map;
  late final int _xSize;
  late final int _ySize;

  HeightMap.parse(String mapString)
      : _map = mapString
            .trim()
            .split('\n')
            .map((row) => row.split('').map(int.parse).toList(growable: false))
            .toList(growable: false) {
    _ySize = _map.length;
    _xSize = _map.isNotEmpty ? _map.first.length : 0;
  }

  Iterable<Pt> adjacentTo(Pt pt) sync* {
    if (pt.y > 0) yield Pt(pt.x, pt.y - 1); // Top
    if (pt.x > 0) yield Pt(pt.x - 1, pt.y); // Left
    if (pt.y < _ySize - 1) yield Pt(pt.x, pt.y + 1); // Bottom
    if (pt.x < _xSize - 1) yield Pt(pt.x + 1, pt.y); // Right
  }

  bool isLowPoint(Pt pt) => adjacentTo(pt)
      .map((adj) => heightAt(pt) < heightAt(adj))
      .reduce((value, element) => value && element);

  Iterable<Pt> lowPoints() sync* {
    for (var y = 0; y < _ySize; y++) {
      for (var x = 0; x < _xSize; x++) {
        final pt = Pt(x, y);
        if (isLowPoint(pt)) yield pt;
      }
    }
  }

  int heightAt(Pt pt) => _map[pt.y][pt.x];

  int riskOf(Pt pt) => 1 + heightAt(pt);

  int get totalRisk =>
      lowPoints().map(riskOf).reduce((value, element) => value + element);

  Iterable<Pt> upstreamOf(Pt pt) sync* {
    for (final adjUpstream
        in adjacentTo(pt).where((adj) => heightAt(adj) > heightAt(pt))) {
      yield adjUpstream;
      for (final farUpstream in upstreamOf(adjUpstream)) {
        yield farUpstream;
      }
    }
  }

  Set<Pt> basinOf(Pt pt) =>
      {pt, ...upstreamOf(pt).where((p) => heightAt(p) < 9)};

  Iterable<int> basinSizes() =>
      lowPoints().map(basinOf).map((basin) => basin.length);
}
