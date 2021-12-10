import 'dart:math';

class FishPopulationModel {
  final int normalCycleLength;
  final int newbornCycleLength;
  final List<int> fishAtStage;

  FishPopulationModel({this.normalCycleLength = 7, this.newbornCycleLength = 9})
      : fishAtStage = List.filled(max(normalCycleLength, newbornCycleLength), 0,
            growable: true);

  int get population => fishAtStage.reduce((value, element) => value + element);

  void addFishAtStage(int stage) {
    fishAtStage[stage] += 1;
  }

  void ffwd(int days) {
    for (var _ = 0; _ < days; _++) {
      final newFish = fishAtStage.removeAt(0);
      fishAtStage.add(0);
      fishAtStage[normalCycleLength - 1] += newFish;
      fishAtStage[newbornCycleLength - 1] = newFish;
    }
  }
}
