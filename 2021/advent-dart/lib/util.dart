import 'dart:io';

List<int> readIntsFromFile(final String fileName) {
  final file = File(fileName);
  return file.readAsLinesSync().map((e) => int.parse(e)).toList();
}
