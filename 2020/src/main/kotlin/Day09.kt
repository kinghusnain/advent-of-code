import java.math.BigInteger

class Day09 {}

fun List<BigInteger>.isValid(i: Int): Boolean {
    if (this.size < 26) {
        throw Exception()
    }
    if (i < 25) {
        return true
    }
    val window = (i-25) until i
    for (j in window) {
        for (k in window) {
            if (j != k && this[j] + this[k] == this[i]) {
                return true
            }
        }
    }
    return false
}

fun List<BigInteger>.contiguousSum(start: Int, targetSum: BigInteger): List<BigInteger> {
    for (end in (start+1)..this.size) {
        if (this[end] > targetSum) {
            return emptyList()
        }
        val sum = this.subList(start, end).sumOf { it }
        if (targetSum == sum) {
            return this.subList(start, end)
        }
    }
    return emptyList()
}

fun main() {
    val input = Day09::javaClass.javaClass.classLoader.getResource("day09.txt")?.readText() ?: ""
    val sequence = input.split("\n").map { it.toBigInteger() }

    var invalid: BigInteger? = null
    for (i in sequence.indices) {
        if (!sequence.isValid(i)) {
            invalid = sequence[i]
            println(invalid)
            break
        }
    }

    if (invalid == null) return
    var subSequence: List<BigInteger>
    for (i in 1..sequence.size) {
        subSequence = sequence.contiguousSum(i, invalid)
        if (subSequence.isNotEmpty()) {
            val min = subSequence.minOrNull() ?: throw Exception()
            val max = subSequence.maxOrNull() ?: throw Exception()
            println(min + max)
            break
        }
    }
}