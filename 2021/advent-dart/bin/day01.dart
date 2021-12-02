import 'package:advent_dart/day01.dart';
import 'package:advent_dart/util.dart';

void main(List<String> args) {
  final input = readIntsFromFile('puzzle_input/day01.txt');
  final part1Soln = countIncreases(input);
  print(part1Soln);
  final part2Soln = countWindowedIncreases(input, 3);
  print(part2Soln);
}
