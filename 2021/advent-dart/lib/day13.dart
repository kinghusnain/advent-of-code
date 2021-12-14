import 'dart:math';

typedef Pt = Point<int>;

class TransparentOrigami {
  final Set<Pt> _dots = {};
  var _xSize = 0;
  var _ySize = 0;

  Set<Pt> get dots => _dots;

  TransparentOrigami.parse(String input) {
    for (final line in input.trim().split('\n')) {
      final pair = line.split(',');
      final x = int.parse(pair[0]);
      final y = int.parse(pair[1]);
      _dots.add(Pt(x, y));
      _xSize = max(_xSize, x + 1);
      _ySize = max(_ySize, y + 1);
    }
  }

  void fold(String instr) {
    const prefix = 'fold along ';
    if (!instr.startsWith(prefix)) throw Exception();
    final pair = instr.substring(prefix.length).split('=');
    final dim = pair[0].trim();
    final coord = int.parse(pair[1]);
    switch (dim) {
      case 'x':
        foldX(coord);
        break;
      case 'y':
        foldY(coord);
        break;
      default:
        throw Exception();
    }
  }

  void foldY(int y) {
    for (final pt in _dots.where((p) => p.y > y).toList()) {
      _dots.remove(pt);
      _dots.add(Pt(pt.x, y - (pt.y - y)));
    }
    _ySize = y;
  }

  void foldX(int x) {
    for (final pt in _dots.where((p) => p.x > x).toList()) {
      _dots.remove(pt);
      _dots.add(Pt(x - (pt.x - x), pt.y));
    }
    _xSize = x;
  }

  @override
  String toString() {
    final buff = StringBuffer();
    for (var y = 0; y < _ySize; y++) {
      for (var x = 0; x < _xSize; x++) {
        buff.write(_dots.contains(Pt(x, y)) ? '#' : '.');
      }
      buff.writeln();
    }
    return buff.toString().trim();
  }
}
