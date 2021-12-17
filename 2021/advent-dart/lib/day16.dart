abstract class PacketType {
  static const sum = 0;
  static const product = 1;
  static const minimum = 2;
  static const maximum = 3;
  static const literal = 4;
  static const greaterThan = 5;
  static const lessThan = 6;
  static const equals = 7;
}

abstract class Packet {
  late final int version;
  late final int type;
  late final String _unparsed;

  int get value;

  static Packet parse(String binString) {
    switch (typeOf(binString)) {
      case PacketType.literal:
        return LiteralPacket.parse(binString);
      case PacketType.sum:
        return OperatorPacket.parse(
          binString,
          operatorFunction: (subPackets) =>
              subPackets.fold(0, (sum, packet) => sum + packet.value),
        );
      case PacketType.product:
        return OperatorPacket.parse(
          binString,
          operatorFunction: (subPackets) =>
              subPackets.fold(1, (product, packet) => product * packet.value),
        );
      case PacketType.minimum:
        return OperatorPacket.parse(
          binString,
          operatorFunction: (subPackets) =>
              subPackets.fold(null, (min, packet) {
            final val = packet.value;
            if (min != null) {
              return val < min ? val : min;
            } else {
              return val;
            }
          })!,
        );
      case PacketType.maximum:
        return OperatorPacket.parse(
          binString,
          operatorFunction: (subPackets) => subPackets.fold(0, (max, packet) {
            final val = packet.value;
            return val > max ? val : max;
          }),
        );
      case PacketType.greaterThan:
        return OperatorPacket.parse(
          binString,
          operatorFunction: (subPackets) =>
              subPackets[0].value > subPackets[1].value ? 1 : 0,
        );
      case PacketType.lessThan:
        return OperatorPacket.parse(
          binString,
          operatorFunction: (subPackets) =>
              subPackets[0].value < subPackets[1].value ? 1 : 0,
        );
      case PacketType.equals:
        return OperatorPacket.parse(
          binString,
          operatorFunction: (subPackets) =>
              subPackets[0].value == subPackets[1].value ? 1 : 0,
        );
      default:
        throw Exception();
    }
  }

  static int versionOf(String binString) =>
      int.parse(binString.substring(0, 3), radix: 2);
  static int typeOf(String binString) =>
      int.parse(binString.substring(3, 6), radix: 2);

  Iterable<Packet> decendPacketTree() sync* {
    yield this;
  }
}

class LiteralPacket extends Packet {
  late final int _value;

  @override
  int get value => _value;

  LiteralPacket.parse(String binString) : super() {
    version = Packet.versionOf(binString);
    type = Packet.typeOf(binString);

    binString = binString.substring(6);
    var v = 0;
    while (binString.startsWith('1')) {
      v *= 16;
      v += int.parse(binString.substring(1, 5), radix: 2);
      binString = binString.substring(5);
    }
    v *= 16;
    v += int.parse(binString.substring(1, 5), radix: 2);

    _value = v;
    _unparsed = binString.substring(5);
  }
}

class OperatorPacket extends Packet {
  final List<Packet> subPackets = [];
  late final int lengthType;
  late final int length;
  final int Function(List<Packet>) _operatorFunction;

  @override
  int get value => _operatorFunction(subPackets);

  OperatorPacket.parse(String binString,
      {required int Function(List<Packet>) operatorFunction})
      : _operatorFunction = operatorFunction,
        super() {
    version = Packet.versionOf(binString);
    type = Packet.typeOf(binString);
    lengthType = lengthTypeOf(binString);

    switch (lengthType) {
      case 0:
        length = length0Of(binString);
        binString = binString.substring(22);
        var bitsRead = 0;
        while (bitsRead < length) {
          final packet = Packet.parse(binString);
          subPackets.add(packet);
          bitsRead += binString.length - packet._unparsed.length;
          binString = packet._unparsed;
        }
        break;
      case 1:
        length = length1Of(binString);
        binString = binString.substring(18);
        while (subPackets.length < length) {
          final packet = Packet.parse(binString);
          subPackets.add(packet);
          binString = packet._unparsed;
        }
        break;
    }

    _unparsed = binString;
  }

  static int lengthTypeOf(String binString) =>
      int.parse(binString.substring(6, 7), radix: 2);
  static int length0Of(String binString) =>
      int.parse(binString.substring(7, 7 + 15), radix: 2);
  static int length1Of(String binString) =>
      int.parse(binString.substring(7, 7 + 11), radix: 2);

  @override
  Iterable<Packet> decendPacketTree() sync* {
    yield this;
    for (final sub in subPackets) {
      for (final packet in sub.decendPacketTree()) {
        yield packet;
      }
    }
  }
}

extension HexToBin on String {
  String hexToBin() => split('')
      .map((c) => int.parse(c, radix: 16).toRadixString(2).padLeft(4, '0'))
      .join('');
}
