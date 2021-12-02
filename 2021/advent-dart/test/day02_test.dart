import 'package:advent_dart/day02.dart';
import 'package:test/test.dart';

void main() {
  final input = '''forward 5
down 5
forward 8
up 3
down 8
forward 2'''
      .split('\n');
  test('Part 1 example', () {
    final commands = commandsFromLines(input);
    final position = calculatePosition(commands);
    expect(position.horizontal * position.depth, 150);
  });

  test('Part 2 example', () {
    final commands = commandsFromLines(input);
    final position = calculatePositionMk2(commands);
    expect(position.horizontal * position.depth, 900);
  });
}
