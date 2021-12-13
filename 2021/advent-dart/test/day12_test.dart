import 'package:advent_dart/day12.dart';
import 'package:test/test.dart';

void main() {
  final input = '''start-A
start-b
A-c
A-b
b-d
A-end
b-end''';

  test('Part 1 example', () {
    final system = CaveSystem.parse(input);
    final paths = system.travelToEndFrom(['start']).toList();
    expect(paths.length, 10);
  });

  test('Part 2 example', () {
    final system = CaveSystem.parse(input);
    final paths = system.travelScenicToEndFrom(['start']).toList();
    expect(paths.length, 36);
  });
}
