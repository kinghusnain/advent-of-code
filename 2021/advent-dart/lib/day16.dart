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
  late final String unparsed;

  static Packet parse(String binString) {
    switch (typeOf(binString)) {
      case PacketType.literal:
        return LiteralPacket.parse(binString);
      case PacketType.sum:
        return SumPacket.parse(binString);
      case PacketType.product:
        return ProductPacket.parse(binString);
      case PacketType.minimum:
        return MinPacket.parse(binString);
      case PacketType.maximum:
        return MaxPacket.parse(binString);
      case PacketType.greaterThan:
        return GreaterThanPacket.parse(binString);
      case PacketType.lessThan:
        return LessThanPacket.parse(binString);
      case PacketType.equals:
        return EqualsPacket.parse(binString);
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

  int eval();
}

class LiteralPacket extends Packet {
  late final int value;

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

    value = v;
    unparsed = binString.substring(5);
  }

  @override
  int eval() => value;
}

class OperatorPacket extends Packet {
  final List<Packet> subPackets = [];
  late final int lengthType;
  late final int length;

  OperatorPacket.parse(String binString) : super() {
    version = Packet.versionOf(binString);
    type = Packet.typeOf(binString);
    lengthType = lengthTypeOf(binString);

    if (lengthType == 0) {
      length = length0Of(binString);
      binString = binString.substring(22);
      var bitsRead = 0;
      while (bitsRead < length) {
        final packet = Packet.parse(binString);
        subPackets.add(packet);
        bitsRead += binString.length - packet.unparsed.length;
        binString = packet.unparsed;
      }
    } else if (lengthType == 1) {
      length = length1Of(binString);
      binString = binString.substring(18);
      while (subPackets.length < length) {
        final packet = Packet.parse(binString);
        subPackets.add(packet);
        binString = packet.unparsed;
      }
    }

    unparsed = binString;
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

  @override
  int eval() {
    throw UnimplementedError();
  }
}

class SumPacket extends OperatorPacket {
  SumPacket.parse(String binString) : super.parse(binString);

  @override
  int eval() => subPackets.fold(0, (sum, packet) => sum + packet.eval());
}

class ProductPacket extends OperatorPacket {
  ProductPacket.parse(String binString) : super.parse(binString);

  @override
  int eval() =>
      subPackets.fold(1, (product, packet) => product * packet.eval());
}

class MinPacket extends OperatorPacket {
  MinPacket.parse(String binString) : super.parse(binString);

  @override
  int eval() => subPackets.fold(null, (int? min, packet) {
        final val = packet.eval();
        if (min != null) {
          return val < min ? val : min;
        } else {
          return val;
        }
      })!;
}

class MaxPacket extends OperatorPacket {
  MaxPacket.parse(String binString) : super.parse(binString);

  @override
  int eval() => subPackets.fold(0, (max, packet) {
        final val = packet.eval();
        return val > max ? val : max;
      });
}

class GreaterThanPacket extends OperatorPacket {
  GreaterThanPacket.parse(String binString) : super.parse(binString) {
    if (subPackets.length != 2) throw Exception();
  }

  @override
  int eval() => subPackets[0].eval() > subPackets[1].eval() ? 1 : 0;
}

class LessThanPacket extends OperatorPacket {
  LessThanPacket.parse(String binString) : super.parse(binString) {
    if (subPackets.length != 2) throw Exception();
  }

  @override
  int eval() => subPackets[0].eval() < subPackets[1].eval() ? 1 : 0;
}

class EqualsPacket extends OperatorPacket {
  EqualsPacket.parse(String binString) : super.parse(binString) {
    if (subPackets.length != 2) throw Exception();
  }

  @override
  int eval() => subPackets[0].eval() == subPackets[1].eval() ? 1 : 0;
}

extension HexToBin on String {
  String hexToBin() => split('')
      .map((c) => int.parse(c, radix: 16).toRadixString(2).padLeft(4, '0'))
      .join('');
}
