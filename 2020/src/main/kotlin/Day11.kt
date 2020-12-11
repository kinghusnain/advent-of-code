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

    private fun isEmptyAndAlone(y: Int, x: Int): Boolean {
        return (seatStatus[y][x] == 'L'
                && adjacentSeats(y, x).none { seat -> seatStatus[seat.first][seat.second] == '#' })
    }

    private fun isCrowded(y: Int, x: Int): Boolean {
        return (seatStatus[y][x] == '#'
                && adjacentSeats(y, x).filter { seat -> seatStatus[seat.first][seat.second] == '#' }.size >= 4)
    }

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
    override fun equals(other: Any?) = toString() == other.toString()
}

class SeatMapV2(private val seatStatus: List<List<Char>>) {
    fun visibleSeats(y: Int, x: Int): List<Pair<Int, Int>> {
        var nwSeat: Pair<Int, Int>? = null
        var nwY = y - 1
        var nwX = x - 1
        while (nwY >= 0 && nwX >= 0) {
            if (seatStatus[nwY][nwX] != '.') {
                nwSeat = Pair(nwY, nwX)
                break
            }
            nwY--
            nwX--
        }

        var nSeat: Pair<Int, Int>? = null
        var nY = y - 1
        while (nY >= 0) {
            if (seatStatus[nY][x] != '.') {
                nSeat = Pair(nY, x)
                break
            }
            nY--
        }

        var neSeat: Pair<Int, Int>? = null
        var neY = y - 1
        var neX = x + 1
        while (neY >= 0 && neX < seatStatus[0].size) {
            if (seatStatus[neY][neX] != '.') {
                neSeat = Pair(neY, neX)
                break
            }
            neY--
            neX++
        }

        var wSeat: Pair<Int, Int>? = null
        var wX = x - 1
        while (wX >= 0) {
            if (seatStatus[y][wX] != '.') {
                wSeat = Pair(y, wX)
                break
            }
            wX--
        }

        var eSeat: Pair<Int, Int>? = null
        var eX = x + 1
        while (eX < seatStatus[0].size) {
            if (seatStatus[y][eX] != '.') {
                eSeat = Pair(y, eX)
                break
            }
            eX++
        }

        var swSeat: Pair<Int, Int>? = null
        var swY = y + 1
        var swX = x - 1
        while (swY < seatStatus.size && swX >= 0) {
            if (seatStatus[swY][swX] != '.') {
                swSeat = Pair(swY, swX)
                break
            }
            swY++
            swX--
        }

        var sSeat: Pair<Int, Int>? = null
        var sY = y + 1
        while (sY < seatStatus.size) {
            if (seatStatus[sY][x] != '.') {
                sSeat = Pair(sY, x)
                break
            }
            sY++
        }

        var seSeat: Pair<Int, Int>? = null
        var seY = y + 1
        var seX = x + 1
        while (seY < seatStatus.size && seX < seatStatus[0].size) {
            if (seatStatus[seY][seX] != '.') {
                seSeat = Pair(seY, seX)
                break
            }
            seY++
            seX++
        }

        return listOfNotNull(nwSeat, nSeat, neSeat, wSeat, eSeat, swSeat, sSeat, seSeat)
    }

    private fun isEmptyAndAlone(y: Int, x: Int): Boolean {
        return (seatStatus[y][x] == 'L'
                && visibleSeats(y, x).none { seat -> seatStatus[seat.first][seat.second] == '#' })
    }

    private fun isCrowded(y: Int, x: Int): Boolean {
        return (seatStatus[y][x] == '#'
                && visibleSeats(y, x).filter { seat -> seatStatus[seat.first][seat.second] == '#' }.size >= 5)
    }

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