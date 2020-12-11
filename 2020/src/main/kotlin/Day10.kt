import java.math.BigInteger

class CompleteAdapterChain(private var adapters: List<Int>) {
    var ones = 0
        private set
    var twos = 0
        private set
    var threes = 1
        private set

    init {
        adapters = adapters.sorted()
        for (i in adapters.indices) {
            val prev = if (i == 0) 0 else adapters[i-1]
            when (adapters[i] - prev) {
                1 -> ones += 1
                2 -> twos += 1
                3 -> threes += 1
                else -> throw Exception()
            }
        }
    }
}

class AdapterCollection(private val adapters: MutableList<Int>) {
    private val numPathCache = emptyMap<Int, BigInteger>().toMutableMap()

    init {
        adapters.add(0)
        adapters.sort()
    }

    fun numPaths(start: Int = 0): BigInteger {
        return if (numPathCache.containsKey(start)) {
            numPathCache[start]!!
        } else {
            when (adapters.size - start) {
                0 -> BigInteger.ZERO
                1 -> BigInteger.ONE
                2 -> if (adapters[start + 1] - adapters[start] <= 3) BigInteger.ONE else BigInteger.ZERO
                else -> {
                    var paths = BigInteger.ZERO
                    if (adapters[start + 1] - adapters[start] <= 3) {
                        paths += numPaths(start + 1)
                    }
                    if (adapters[start + 2] - adapters[start] <= 3) {
                        paths += numPaths(start + 2)
                    }
                    if ((adapters.size - start) > 3 && adapters[start + 3] - adapters[start] <= 3) {
                        paths += numPaths(start + 3)
                    }
                    numPathCache[start] = paths
                    paths
                }
            }
        }
    }
}

fun main() {
    val input = CompleteAdapterChain::javaClass.javaClass.classLoader.getResource("day10.txt")?.readText() ?: ""
    val adapters = input.split("\n").map { it.toInt() }

    val chain1 = CompleteAdapterChain(adapters)
    println(chain1.ones * chain1.threes)

    val paths = AdapterCollection(adapters.toMutableList()).numPaths()
    println(paths)
}