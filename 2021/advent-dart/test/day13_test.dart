import 'package:advent_dart/day13.dart';
import 'package:test/test.dart';

void main() {
  final input = '''6,10
0,14
9,10
0,3
10,4
4,11
6,0
6,12
4,1
0,13
10,12
3,4
3,0
8,4
1,10
2,14
8,10
9,0

fold along y=7
fold along x=5''';

  test('Part 1 example', () {
    final inputPair = input.trim().split('\n\n');
    final dotsInput = inputPair[0].trim();
    final origami = TransparentOrigami.parse(dotsInput);
    expect(origami.toString(), '''...#..#..#.
....#......
...........
#..........
...#....#.#
...........
...........
...........
...........
...........
.#....#.##.
....#......
......#...#
#..........
#.#........''');
    final foldInput = inputPair[1].trim();
    final instr = foldInput.split('\n').first;
    origami.fold(instr);
    expect(origami.dots.length, 17);
  });

  test('Part 2 example', () {
    final inputPair = input.trim().split('\n\n');
    final dotsInput = inputPair[0].trim();
    final origami = TransparentOrigami.parse(dotsInput);
    final foldInput = inputPair[1].trim();
    for (final instr in foldInput.split('\n')) {
      origami.fold(instr);
    }
    expect(origami.toString(), '''#####
#...#
#...#
#...#
#####
.....
.....''');
  });
}
