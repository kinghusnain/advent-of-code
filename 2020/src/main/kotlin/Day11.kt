class SeatMap(private val seatStatus: List<List<Char>>) {
    private fun adjacentSeats(y: Int, x: Int) =
        listOf(y - 1, y, y + 1)
            .filter { y2 -> (y2 < seatStatus.size) && (y2 >= 0) }
            .map { y2 ->
                listOf(x - 1, x, x + 1)
                    .filter { x2 -> (x2 < seatStatus[0].size) && (x2 >= 0) }
                    .map { x2 -> Pair(y2, x2) }
            }
            .flatten()
            .filter { it != Pair(y, x) }

    private fun isEmptyAndAlone(y: Int, x: Int) =
        (seatStatus[y][x] == 'L'
                && adjacentSeats(y, x).none { seat -> seatStatus[seat.first][seat.second] == '#' })

    private fun isCrowded(y: Int, x: Int) =
        (seatStatus[y][x] == '#'
                && adjacentSeats(y, x).filter { seat -> seatStatus[seat.first][seat.second] == '#' }.size >= 4)

    fun next(): SeatMap {
        val after = seatStatus.map { it.map { c -> c }.toMutableList() }.toMutableList()
        for (y in seatStatus.indices) {
            for (x in seatStatus[0].indices)  {
                after[y][x] = when {
                    isEmptyAndAlone(y, x) -> '#'
                    isCrowded(y, x) -> 'L'
                    else -> seatStatus[y][x]
                }
            }
        }
        return SeatMap(after)
    }

    override fun toString() = seatStatus.joinToString("") { it.joinToString("") }
    override fun hashCode() = toString().hashCode()
    override fun equals(other: Any?) = toString() == other.toString()
}

class SeatMapV2(private val seatStatus: List<List<Char>>) {
    private fun visibleSeats(y: Int, x: Int) = listOfNotNull(
        visibleNW(y, x), visibleN(y, x), visibleNE(y, x),
        visibleW(y, x), visibleE(y, x),
        visibleSW(y, x), visibleS(y, x), visibleSE(y, x)
    )

    private fun visibleNW(y: Int, x: Int): Pair<Int, Int>? {
        var nwY = y - 1
        var nwX = x - 1
        while (nwY >= 0 && nwX >= 0) {
            if (seatStatus[nwY][nwX] != '.') {
                return Pair(nwY, nwX)
            }
            nwY--
            nwX--
        }
        return null
    }

    private fun visibleN(y: Int, x: Int): Pair<Int, Int>? {
        var nY = y - 1
        while (nY >= 0) {
            if (seatStatus[nY][x] != '.') {
                return Pair(nY, x)
            }
            nY--
        }
        return null
    }

    private fun visibleNE(y: Int, x: Int): Pair<Int, Int>? {
        var neY = y - 1
        var neX = x + 1
        while (neY >= 0 && neX < seatStatus[0].size) {
            if (seatStatus[neY][neX] != '.') {
                return Pair(neY, neX)
            }
            neY--
            neX++
        }
        return null
    }

    private fun visibleW(y: Int, x: Int): Pair<Int, Int>? {
        var wX = x - 1
        while (wX >= 0) {
            if (seatStatus[y][wX] != '.') {
                return Pair(y, wX)
            }
            wX--
        }
        return null
    }

    private fun visibleE(y: Int, x: Int): Pair<Int, Int>? {
        var eX = x + 1
        while (eX < seatStatus[0].size) {
            if (seatStatus[y][eX] != '.') {
                return Pair(y, eX)
            }
            eX++
        }
        return null
    }

    private fun visibleSW(y: Int, x: Int): Pair<Int, Int>? {
        var swY = y + 1
        var swX = x - 1
        while (swY < seatStatus.size && swX >= 0) {
            if (seatStatus[swY][swX] != '.') {
                return Pair(swY, swX)
            }
            swY++
            swX--
        }
        return null
    }

    private fun visibleS(y: Int, x: Int): Pair<Int, Int>? {
        var sY = y + 1
        while (sY < seatStatus.size) {
            if (seatStatus[sY][x] != '.') {
                return Pair(sY, x)
            }
            sY++
        }
        return null
    }

    private fun visibleSE(y: Int, x: Int): Pair<Int, Int>? {
        var seY = y + 1
        var seX = x + 1
        while (seY < seatStatus.size && seX < seatStatus[0].size) {
            if (seatStatus[seY][seX] != '.') {
                return Pair(seY, seX)
            }
            seY++
            seX++
        }
        return null
    }

    private fun isEmptyAndAlone(y: Int, x: Int) =
        (seatStatus[y][x] == 'L'
                && visibleSeats(y, x).none { seat -> seatStatus[seat.first][seat.second] == '#' })

    private fun isCrowded(y: Int, x: Int) =
        (seatStatus[y][x] == '#'
                && visibleSeats(y, x).filter { seat -> seatStatus[seat.first][seat.second] == '#' }.size >= 5)

    fun next(): SeatMapV2 {
        val after = seatStatus.map { it.map { c -> c }.toMutableList() }.toMutableList()
        for (y in seatStatus.indices) {
            for (x in seatStatus[0].indices)  {
                after[y][x] = when {
                    isEmptyAndAlone(y, x) -> '#'
                    isCrowded(y, x) -> 'L'
                    else -> seatStatus[y][x]
                }
            }
        }
        return SeatMapV2(after)
    }

    override fun toString() = seatStatus.joinToString("") { it.joinToString("") }
    override fun hashCode() = toString().hashCode()
    override fun equals(other: Any?) = toString() == other.toString()
}


fun main() {
    val input = SeatMap::javaClass.javaClass.classLoader.getResource("day11.txt")?.readText() ?: ""
    val seats = input.split("\n").map { it.toList() }

    var before = SeatMap(seats)
    var after = before.next()
    while (before != after) {
        before = after
        after = after.next()
    }
    println(after.toString().filter { it == '#' }.length)

    var before2 = SeatMapV2(seats)
    var after2 = before2.next()
    while (before2 != after2) {
        before2 = after2
        after2 = after2.next()
    }
    println(after2.toString().filter { it == '#' }.length)
}