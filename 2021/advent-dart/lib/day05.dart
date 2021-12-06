import 'dart:math';

class Point {
  final int x;
  final int y;

  Point(this.x, this.y);
  Point.parse(String str)
      : x = int.parse(str.split(',')[0]),
        y = int.parse(str.split(',')[1]);

  @override
  String toString() => '$x,$y';
}

class LineSegment {
  final Point start;
  final Point end;

  LineSegment(this.start, this.end);
  LineSegment.parse(String str)
      : start = Point.parse(str.split('->')[0]),
        end = Point.parse(str.split('->')[1]);

  bool get isVertical => start.x == end.x;
  bool get isHorizontal => start.y == end.y;

  @override
  String toString() => '$start -> $end';

  Iterable<Point> points() sync* {
    if (isVertical) {
      for (var y = min(start.y, end.y); y <= max(start.y, end.y); y++) {
        yield Point(start.x, y);
      }
    } else if (isHorizontal) {
      for (var x = min(start.x, end.x); x <= max(start.x, end.x); x++) {
        yield Point(x, start.y);
      }
    } else {
      final deltaX = start.x - end.x > 0 ? -1 : 1;
      final deltaY = start.y - end.y > 0 ? -1 : 1;
      var x = start.x;
      var y = start.y;
      while (x != end.x) {
        yield Point(x, y);
        x += deltaX;
        y += deltaY;
      }
      yield Point(x, y);
    }
  }
}

extension DangerMapping on Iterable<LineSegment> {
  Map<String, int> get dangerRatings {
    final ratings = <String, int>{};
    for (final segment in this) {
      for (final point in segment.points()) {
        ratings[point.toString()] = (ratings[point.toString()] ?? 0) + 1;
      }
    }
    return ratings;
  }
}
