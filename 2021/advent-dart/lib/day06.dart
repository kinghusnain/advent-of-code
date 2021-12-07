import 'dart:math';

class FishPopulationModel {
  final int normalCycleLength;
  final int newbornCycleLength;
  final List<int> fishAtStage;

  FishPopulationModel({this.normalCycleLength = 7, this.newbornCycleLength = 9})
      : fishAtStage =
            List.filled(max(normalCycleLength, newbornCycleLength), 0);

  int get population => fishAtStage.reduce((value, element) => value + element);

  void addFishAtStage(int stage) {
    fishAtStage[stage] += 1;
  }

  void ffwd(int days) {
    for (var d = 0; d < days; d++) {
      final newFish = fishAtStage[0];
      for (var i = 0; i < fishAtStage.length - 1; i++) {
        fishAtStage[i] = fishAtStage[i + 1];
      }
      fishAtStage[normalCycleLength - 1] += newFish;
      fishAtStage[newbornCycleLength - 1] = newFish;
    }
  }
}
