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

  test('Part 2 example', () {
    final scores = input
        .split('\n')
        .where((chunk) => errorScore(chunk) == 0)
        .map(autoCompleteScore)
        .toList();
    expect(scores[0], 288957);
    expect(scores[1], 5566);
    expect(scores[2], 1480781);
    expect(scores[3], 995444);
    expect(scores[4], 294);
    scores.sort();
    final middleScore = scores[scores.length ~/ 2];
    expect(middleScore, 288957);
  });
}
