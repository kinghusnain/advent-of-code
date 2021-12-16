abstract class PacketType {
  static const literal = 4;
}

class Packet {
  late final int version;
  late final int type;
  late final String unparsed;

  static Packet parse(String binString) {
    switch (typeOf(binString)) {
      case PacketType.literal:
        return LiteralPacket.parse(binString);
      default:
        return OperatorPacket.parse(binString);
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
}

extension HexToBin on String {
  String hexToBin() => split('')
      .map((c) => int.parse(c, radix: 16).toRadixString(2).padLeft(4, '0'))
      .join('');
}
