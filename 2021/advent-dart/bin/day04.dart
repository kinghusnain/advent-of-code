import 'dart:io';

import 'package:advent_dart/day04.dart';

void main(List<String> args) {
  final input = File('puzzle_input/day04.txt').readAsLinesSync();
  final picks = input.first.trim().split(',').map((e) => int.parse(e));
  var boards = <BingoBoard>[];
  var boardStrings = <String>[];
  input.sublist(1).skipWhile((value) => value.trim() == '').forEach((line) {
    if (line.trim() == '') {
      boards.add(BingoBoard.fromStrings(boardStrings));
      boardStrings = <String>[];
    } else {
      boardStrings.add(line.trim());
    }
  });
  if (boardStrings.isNotEmpty) {
    boards.add(BingoBoard.fromStrings(boardStrings));
  }
  final winningScore = playUntilWinner(boards, picks) ?? -1;
  print(winningScore);

  boards = <BingoBoard>[];
  boardStrings = <String>[];
  input.sublist(1).skipWhile((value) => value.trim() == '').forEach((line) {
    if (line.trim() == '') {
      boards.add(BingoBoard.fromStrings(boardStrings));
      boardStrings = <String>[];
    } else {
      boardStrings.add(line.trim());
    }
  });
  if (boardStrings.isNotEmpty) {
    boards.add(BingoBoard.fromStrings(boardStrings));
  }
  final losingScore = playUntilLoser(boards, picks) ?? -1;
  print(losingScore);
}
