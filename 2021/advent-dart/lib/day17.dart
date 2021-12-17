class TargetArea {
  final int xMin;
  final int xMax;
  final int yMin;
  final int yMax;

  TargetArea(this.xMin, this.xMax, this.yMin, this.yMax);

  bool containsPos(int xPos, int yPos) =>
      xMin <= xPos && xPos <= xMax && yMin <= yPos && yPos <= yMax;
}

class Velocity {
  final int x;
  final int y;

  Velocity(this.x, this.y);

  @override
  bool operator ==(Object other) =>
      other is Velocity && x == other.x && y == other.y;

  @override
  int get hashCode => 1000000 * y + x; // Good enough?

  @override
  String toString() => '$x,$y';
}

class Result {
  final Velocity startingVelocity;
  final bool hitTarget;
  final int apex;
  final int distance;

  Result(this.startingVelocity, this.hitTarget, this.apex, this.distance);
}

Result testFire(Velocity startingVelocity, TargetArea target) {
  var apex = 0;
  var distance = 0;
  var hit = false;

  var xVeloc = startingVelocity.x;
  var yVeloc = startingVelocity.y;
  var xPos = 0;
  var yPos = 0;
  while (yPos >= target.yMin) {
    xPos += xVeloc;
    yPos += yVeloc;
    if (xVeloc != 0) xVeloc += xVeloc > 0 ? -1 : 1;
    yVeloc -= 1;

    if (yPos > apex) apex = yPos;
    if (xPos > distance) distance = xPos;
    if (target.containsPos(xPos, yPos)) hit = true;
  }

  return Result(startingVelocity, hit, apex, distance);
}

Iterable<Result> findGoodResults(TargetArea target) sync* {
  for (var x = 0; x <= target.xMax; x++) {
    const maxY = 1000; // How do I find this???
    for (var y = 0; y < maxY; y++) {
      var result = testFire(Velocity(x, y), target);
      if (result.hitTarget) yield result;

      result = testFire(Velocity(x, -y), target);
      if (result.hitTarget) yield result;
    }
  }
}

Iterable<Velocity> findGoodVelocities(TargetArea target) =>
    findGoodResults(target).map((r) => r.startingVelocity);

int bestApex(TargetArea target) => findGoodResults(target)
    .fold(
      Result(Velocity(0, 0), false, 0, 0),
      (Result r1, Result r2) => r1.apex > r2.apex ? r1 : r2,
    )
    .apex;
