class PocketDimension3D {
    val activationState: MutableMap<Int, MutableMap<Int, MutableMap<Int, Boolean>>> = mutableMapOf()

    fun isActive(x: Int, y: Int, z: Int) =
        activationState.get(x)?.get(y)?.get(z) ?: false

    fun setState(x: Int, y: Int, z: Int, state: Boolean) {
        when {
            x !in activationState.keys -> {
                activationState[x] = mutableMapOf(
                    y to mutableMapOf(
                        z to state
                    )
                )
            }
            y !in activationState[x]!!.keys -> {
                activationState[x]!![y] = mutableMapOf(z to state)
            }
            else -> {
                activationState[x]!![y]!![z] = state
            }
        }
    }

    fun activeCount() =
        activationState.map { xs -> xs.value.map { ys -> ys.value.filter { it.value }.count() }.sum() }.sum()

    fun load2D(state: String) {
        val rows = state.split("\n")
        for (y in rows.indices) {
            for (x in rows[y].indices) {
                setState(x, y, 0, rows[y][x] == '#')
            }
        }
    }

    fun next(): PocketDimension3D {
        val nextDimension = PocketDimension3D()
        val xRange = activationState.keys.toMutableList()
        val xMin = xRange.minOrNull() ?: throw Exception()
        val xMax = xRange.maxOrNull() ?: throw Exception()
        xRange.add(xMin-1)
        xRange.add(xMax+1)
        for (x in xRange) {
            val yRange = activationState[0]!!.keys.toMutableList()
            val yMin = yRange.minOrNull() ?: throw Exception()
            val yMax = yRange.maxOrNull() ?: throw Exception()
            yRange.add(yMin-1)
            yRange.add(yMax+1)
            for (y in yRange) {
                val zRange = activationState[0]!![0]!!.keys.toMutableList()
                val zMin = zRange.minOrNull() ?: throw Exception()
                val zMax = zRange.maxOrNull() ?: throw Exception()
                zRange.add(zMin-1)
                zRange.add(zMax+1)
                for (z in zRange) {
                    val neighbors = listOf(x-1, x, x+1)
                        .map { xc -> listOf(Pair(xc, y-1), Pair(xc, y), Pair(xc, y+1)) }
                        .flatten()
                        .map { xy ->
                            listOf(
                                Triple(xy.first, xy.second, z-1),
                                Triple(xy.first, xy.second, z),
                                Triple(xy.first, xy.second, z+1)
                            )
                        }
                        .flatten()
                        .filter { it != Triple(x, y, z) }
                    val neighborStates = neighbors.map { isActive(it.first, it.second, it.third) }
                    val activeNeighbors = neighborStates.filter { it }.size
                    if (isActive(x, y, z)) {
                        val nextState = activeNeighbors in listOf(2, 3)
                        nextDimension.setState(x, y, z, nextState)
                    } else {
                        nextDimension.setState(x, y, z, activeNeighbors == 3)
                    }
                }
            }
        }
        return nextDimension
    }
}

class PocketDimension4D {
    val activationState: MutableMap<Int, MutableMap<Int, MutableMap<Int, MutableMap<Int, Boolean>>>> = mutableMapOf()

    fun isActive(x: Int, y: Int, z: Int, w: Int) =
        activationState.get(x)?.get(y)?.get(z)?.get(w) ?: false

    fun setState(x: Int, y: Int, z: Int, w: Int, state: Boolean) {
        when {
            x !in activationState.keys -> {
                activationState[x] = mutableMapOf(
                    y to mutableMapOf(
                        z to mutableMapOf(
                            w to state
                        )
                    )
                )
            }
            y !in activationState[x]!!.keys -> {
                activationState[x]!![y] = mutableMapOf(z to mutableMapOf(w to state))
            }
            z !in activationState[x]!![y]!!.keys -> {
                activationState[x]!![y]!![z] = mutableMapOf(w to state)
            }
            else -> {
                activationState[x]!![y]!![z]!![w] = state
            }
        }
    }

    fun activeCount() =
        activationState.map { xs ->
            xs.value.map { ys ->
                ys.value.map { zs ->
                    zs.value.filter { it.value }.count()
                }.sum()
            }.sum()
        }.sum()

    fun load2D(state: String) {
        val rows = state.split("\n")
        for (y in rows.indices) {
            for (x in rows[y].indices) {
                setState(x, y, 0, 0,  rows[y][x] == '#')
            }
        }
    }

    fun next(): PocketDimension4D {
        val nextDimension = PocketDimension4D()
        val xRange = activationState.keys.toMutableList()
        val xMin = xRange.minOrNull() ?: throw Exception()
        val xMax = xRange.maxOrNull() ?: throw Exception()
        xRange.add(xMin-1)
        xRange.add(xMax+1)
        for (x in xRange) {
            val yRange = activationState[0]!!.keys.toMutableList()
            val yMin = yRange.minOrNull() ?: throw Exception()
            val yMax = yRange.maxOrNull() ?: throw Exception()
            yRange.add(yMin-1)
            yRange.add(yMax+1)
            for (y in yRange) {
                val zRange = activationState[0]!![0]!!.keys.toMutableList()
                val zMin = zRange.minOrNull() ?: throw Exception()
                val zMax = zRange.maxOrNull() ?: throw Exception()
                zRange.add(zMin-1)
                zRange.add(zMax+1)
                for (z in zRange) {
                    val wRange = activationState[0]!![0]!![0]!!.keys.toMutableList()
                    val wMin = wRange.minOrNull() ?: throw Exception()
                    val wMax = wRange.maxOrNull() ?: throw Exception()
                    wRange.add(wMin-1)
                    wRange.add(wMax+1)
                    for (w in wRange) {
                        val neighbors = listOf(x - 1, x, x + 1)
                            .map { xc -> listOf(Pair(xc, y - 1), Pair(xc, y), Pair(xc, y + 1)) }
                            .flatten()
                            .map { xy ->
                                listOf(
                                    Triple(xy.first, xy.second, z - 1),
                                    Triple(xy.first, xy.second, z),
                                    Triple(xy.first, xy.second, z + 1)
                                )
                            }
                            .flatten()
                            .map { xyz ->
                                listOf(
                                    listOf(xyz.first, xyz.second, xyz.third, w - 1),
                                    listOf(xyz.first, xyz.second, xyz.third, w),
                                    listOf(xyz.first, xyz.second, xyz.third, w + 1)
                                )
                            }
                            .flatten()
                            .filter { it != listOf(x, y, z, w) }
                        val neighborStates = neighbors.map { isActive(it[0], it[1], it[2], it[3]) }
                        val activeNeighbors = neighborStates.filter { it }.size
                        if (isActive(x, y, z, w)) {
                            val nextState = activeNeighbors in listOf(2, 3)
                            nextDimension.setState(x, y, z, w, nextState)
                        } else {
                            nextDimension.setState(x, y, z, w, activeNeighbors == 3)
                        }
                    }
                }
            }
        }
        return nextDimension
    }
}

fun main() {
    val input = """.#..####
.#.#...#
#..#.#.#
###..##.
..##...#
..##.###
#.....#.
..##..##"""
    val pd0 = PocketDimension3D()
    pd0.load2D(input)
    val pd6 = pd0.next().next().next().next().next().next()
    println(pd6.activeCount())

    val pd4d0 = PocketDimension4D()
    pd4d0.load2D(input)
    val pd4d6 = pd4d0.next().next().next().next().next().next()
    println(pd4d6.activeCount())
}