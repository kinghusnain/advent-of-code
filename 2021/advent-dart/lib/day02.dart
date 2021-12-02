class Position {
  int horizontal = 0;
  int depth = 0;
}

class Command {
  final Direction direction;
  final int magnitude;

  Command(this.direction, this.magnitude);
}

enum Direction { forward, up, down }

Position calculatePosition(Iterable<Command> course) {
  Position position = Position();

  for (final command in course) {
    switch (command.direction) {
      case Direction.forward:
        position.horizontal += command.magnitude;
        break;
      case Direction.down:
        position.depth += command.magnitude;
        break;
      case Direction.up:
        position.depth -= command.magnitude;
        break;
    }
  }

  return position;
}

Iterable<Command> commandsFromLines(Iterable<String> lines) =>
    lines.map((line) {
      final tokens = line.split(' ');
      if (tokens.length < 2) throw FormatException();

      final magnitude = int.parse(tokens[1]);
      final command = tokens[0];
      switch (command) {
        case 'forward':
          return Command(Direction.forward, magnitude);
        case 'up':
          return Command(Direction.up, magnitude);
        case 'down':
          return Command(Direction.down, magnitude);
        default:
          throw FormatException();
      }
    });
