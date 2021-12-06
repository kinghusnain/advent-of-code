class BingoBoard {
  final List<List<int>> numbers;
  late final List<List<bool>> marked;
  int score = 0;
  bool inPlay = true;
  late int _sumOfUnMarked;

  BingoBoard(this.numbers)
      : marked =
            List.filled(numbers.length, List.filled(numbers.length, false)),
        _sumOfUnMarked = numbers
            .map((row) => row.reduce((value, element) => value + element))
            .reduce((value, element) => value + element);

  BingoBoard.fromStrings(List<String> strings) : numbers = <List<int>>[] {
    for (final line in strings) {
      if (line.trim() == '') continue;
      var row = line.split(RegExp(r'\s+')).map((e) => int.parse(e)).toList();
      numbers.add(row);
    }
    marked = List.generate(
        numbers.length, (_) => List.filled(numbers.length, false));
    _sumOfUnMarked = numbers
        .map((row) => row.reduce((value, element) => value + element))
        .reduce((value, element) => value + element);
  }

  bool get isWinner {
    for (final row in marked) {
      if (row.reduce((value, element) => value && element)) return true;
    }
    for (var c = 0; c < numbers.length; c++) {
      var columnMarked = true;
      for (var r = 0; r < numbers.length; r++) {
        columnMarked &= marked[r][c];
      }
      if (columnMarked) return true;
    }
    return false;
  }

  void mark(int number) {
    for (var column = 0; column < numbers.length; column++) {
      for (var row = 0; row < numbers.length; row++) {
        if (numbers[row][column] == number) {
          marked[row][column] = true;
          _sumOfUnMarked -= number;
        }
      }
    }
    score = number * _sumOfUnMarked;
  }
}

int? playUntilWinner(Iterable<BingoBoard> boards, Iterable<int> picks) {
  for (final n in picks) {
    for (final board in boards) {
      board.mark(n);
      if (board.isWinner) {
        return board.score;
      }
    }
  }
}

int? playUntilLoser(Iterable<BingoBoard> boards, Iterable<int> picks) {
  var remaining = boards.length;
  for (final n in picks) {
    for (final board in boards) {
      if (board.inPlay) {
        board.mark(n);
        if (board.isWinner) {
          board.inPlay = false;
          remaining -= 1;
          if (remaining == 0) return board.score;
        }
      }
    }
  }
}
