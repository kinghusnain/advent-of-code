
enum class TileColor { BLACK, WHITE }

class HexGrid {
    private val tiles: MutableMap<Int, MutableMap<Int, TileColor>> = mutableMapOf()

    private fun nw(x: Int, y: Int) = Pair(x, y + 1)
    private fun ne(x: Int, y: Int) = Pair(x + 1, y + 1)
    private fun w(x: Int, y: Int) = Pair(x - 1, y)
    private fun e(x: Int, y: Int) = Pair(x + 1, y)
    private fun sw(x: Int, y: Int) = Pair(x - 1, y - 1)
    private fun se(x: Int, y: Int) = Pair(x, y - 1)

    private fun getTileColor(x: Int, y: Int) = when {
        x !in tiles.keys -> TileColor.WHITE
        y !in tiles[x]!!.keys -> TileColor.WHITE
        else -> tiles[x]!![y]!!
    }

    private fun setTileColor(x: Int, y: Int, color: TileColor) {
        when (x) {
            !in tiles.keys -> tiles[x] = mutableMapOf(y to color)
            else -> tiles[x]!![y] = color
        }
    }

    private fun flipTile(x: Int, y: Int) {
        val color = if (getTileColor(x, y) == TileColor.WHITE) {
            TileColor.BLACK
        } else {
            TileColor.WHITE
        }
        setTileColor(x, y, color)
    }

    fun blackTileCount() = tiles.values.map { it.values.map { c -> c } }
        .flatten()
        .filter { it == TileColor.BLACK }
        .count()

    fun expand() {
        val xs = tiles.keys.toMutableList()
        xs.add(xs.minOrNull()!! - 1)
        xs.add(xs.maxOrNull()!! + 1)

        val ys = tiles.values.map { it.keys }.flatten().toSet().toMutableList()
        ys.add(ys.minOrNull()!! - 1)
        ys.add(ys.maxOrNull()!! + 1)

        for (x in xs) {
            for (y in ys) {
                setTileColor(x, y, getTileColor(x, y))
            }
        }
    }

    fun dailyFlips() {
        val flips = mutableListOf<Pair<Int, Int>>()

        expand()
        tiles.forEach { (x, ys) ->
            ys.forEach { (y, c) ->
                var adjacentBlack = 0

                if (getTileColor(nw(x, y).first, nw(x, y).second) == TileColor.BLACK)
                    adjacentBlack += 1
                if (getTileColor(ne(x, y).first, ne(x, y).second) == TileColor.BLACK)
                    adjacentBlack += 1
                if (getTileColor(w(x, y).first, w(x, y).second) == TileColor.BLACK)
                    adjacentBlack += 1
                if (getTileColor(e(x, y).first, e(x, y).second) == TileColor.BLACK)
                    adjacentBlack += 1
                if (getTileColor(sw(x, y).first, sw(x, y).second) == TileColor.BLACK)
                    adjacentBlack += 1
                if (getTileColor(se(x, y).first, se(x, y).second) == TileColor.BLACK)
                    adjacentBlack += 1

                if (c == TileColor.BLACK && (adjacentBlack == 0 || adjacentBlack > 2)) {
                    flips.add(Pair(x, y))
                } else if (c == TileColor.WHITE && (adjacentBlack == 2)) {
                    flips.add(Pair(x, y))
                }
            }
        }

        flips.forEach { xy -> flipTile(xy.first, xy.second) }
    }

    fun flipTiles(tileDirections: List<String>) {
        tileDirections.forEach { s: String ->
            var xy = Pair(0, 0)
            var dirs = s
            while (dirs.isNotBlank()) {
                when {
                    dirs.substring(0, 1) == "e" -> {
                        xy = this.e(xy.first, xy.second)
                        dirs = dirs.substring(1)
                    }
                    dirs.substring(0, 1) == "w" -> {
                        xy = this.w(xy.first, xy.second)
                        dirs = dirs.substring(1)
                    }
                    dirs.substring(0, 2) == "nw" -> {
                        xy = this.nw(xy.first, xy.second)
                        dirs = dirs.substring(2)
                    }
                    dirs.substring(0, 2) == "ne" -> {
                        xy = this.ne(xy.first, xy.second)
                        dirs = dirs.substring(2)
                    }
                    dirs.substring(0, 2) == "sw" -> {
                        xy = this.sw(xy.first, xy.second)
                        dirs = dirs.substring(2)
                    }
                    dirs.substring(0, 2) == "se" -> {
                        xy = this.se(xy.first, xy.second)
                        dirs = dirs.substring(2)
                    }
                    else -> throw Exception()
                }
            }
            this.flipTile(xy.first, xy.second)
        }
    }
}

fun main() {
    val input = HexGrid::javaClass.javaClass.classLoader.getResource("day24.txt")?.readText() ?: ""

    val tileGrid = HexGrid()
    tileGrid.flipTiles(input.split("\n"))
    println(tileGrid.blackTileCount())

    for (n in 1..100) {
        tileGrid.dailyFlips()
    }
    println(tileGrid.blackTileCount())
}