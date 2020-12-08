class Day05 {}

fun findRow(str: String, low: Int, high: Int): Int = when {
    str.isEmpty() -> low
    str[0] == 'F' -> findRow(str.substring(1), low, low + (high - low) / 2)
    str[0] == 'B' -> findRow(str.substring(1), low + (high - low) / 2, high)
    else -> throw Exception()
}

fun findCol(str: String, low: Int, high: Int): Int = when {
    str.isEmpty() -> low
    str[0] == 'L' -> findCol(str.substring(1), low, low + (high - low) / 2)
    str[0] == 'R' -> findCol(str.substring(1), low + (high - low) / 2, high)
    else -> throw Exception()
}

fun findSeat(str: String) = 8 * findRow(str.substring(0..6), 0, 128) +
    findCol(str.substring(7), 0, 8)

fun main() {
    val input = Day05::javaClass.javaClass.classLoader.getResource("day05.txt")?.readText() ?: ""
    val seatIDs = input.split("\n").map { findSeat(it) }
    println(seatIDs.maxOrNull())

    val firstSeat = seatIDs.minOrNull() ?: throw Exception()
    val lastSeat = seatIDs.maxOrNull() ?: throw Exception()
    val mySeat = (firstSeat..lastSeat).toSet() subtract seatIDs.toSet()
    println(mySeat)
}