class ElfGame(startingNumbers: List<Int>) {
    private val numbers = startingNumbers.toMutableList()

    private fun next() {
        val last = numbers.last()
        val lastIndex = numbers.subList(0, numbers.size-1).lastIndexOf(last)
        numbers.add(if (lastIndex == -1) 0 else (numbers.size - 1 - lastIndex))
    }

    fun getTurn(t: Int): Int {
        while (numbers.size < t) next()
        return numbers[t-1]
    }
}

class ElfGame2(startingNumbers: List<Int>) {
    private val lastSeen = mutableMapOf<Int, Int>()
    private var last = startingNumbers.last()
    private var lastIndex = startingNumbers.size

    init {
        for (i in 0 until startingNumbers.size-1) {
            lastSeen[startingNumbers[i]] = i + 1
        }
    }

    private fun next() {
        if (last in lastSeen.keys) {
            val idx = lastSeen[last]!!
            lastSeen[last] = lastIndex
            last = lastIndex - idx
        } else {
            lastSeen[last] = lastIndex
            last = 0
        }
        lastIndex += 1
    }

    fun getTurn(t: Int): Int {
        while (lastIndex < t) next()
        return last
    }
}

fun main() {
    println(ElfGame(listOf(6,3,15,13,1,0)).getTurn(2020))
    println(ElfGame2(listOf(6,3,15,13,1,0)).getTurn(2020))
    println(ElfGame2(listOf(6,3,15,13,1,0)).getTurn(30000000))
}