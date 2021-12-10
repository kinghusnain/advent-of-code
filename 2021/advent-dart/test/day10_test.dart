import 'package:advent_dart/day10.dart';
import 'package:test/test.dart';

void main() {
  final input = '''[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]''';

  test('Part 1 example', () {
    final totalScore = input
        .split('\n')
        .map(errorScore)
        .reduce((value, element) => value + element);
    expect(totalScore, 26397);
  });
}
