typedef Cave = String;

extension CaveMethods on Cave {
  bool get isSmall => this == toLowerCase();
  bool get isLarge => this != toLowerCase();
}

typedef Path = List<Cave>;

class CaveSystem {
  final Map<Cave, List<Cave>> _exits = {};

  CaveSystem.parse(String input) {
    for (final line in input.trim().split('\n')) {
      final pair = line.split('-');
      final Cave cave = pair[0];
      final Cave exit = pair[1];
      _exits[cave] = (_exits[cave] ?? []) + [exit];
      _exits[exit] = (_exits[exit] ?? []) + [cave];
    }
  }

  Iterable<Path> travelToEndFrom(Path path) sync* {
    if (path.last == 'end') yield path;
    final exits = _exits[path.last]
            ?.where((exit) => exit.isLarge || !path.contains(exit)) ??
        [];
    for (final exit in exits) {
      final extendedPath = path + [exit];
      for (final path in travelToEndFrom(extendedPath)) {
        yield path;
      }
    }
  }

  Iterable<Path> travelScenicToEndFrom(Path path) sync* {
    if (path.last == 'end') {
      yield path;
    } else {
      final smallCavesVisitedTwice = path.where(
          (cave) => cave.isSmall && path.where((e) => e == cave).length == 2);
      final exits = _exits[path.last]?.where((exit) => exit != 'start').where(
              (exit) =>
                  exit.isLarge ||
                  !path.contains(exit) ||
                  smallCavesVisitedTwice.isEmpty) ??
          [];
      for (final exit in exits) {
        final extendedPath = path + [exit];
        for (final path in travelScenicToEndFrom(extendedPath)) {
          yield path;
        }
      }
    }
  }
}
