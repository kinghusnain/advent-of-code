import java.math.BigInteger

class Day09 {}

fun List<BigInteger>.isValid(i: Int): Boolean {
    if (this.size < 26) { throw Exception() }
    if (i < 25) { return true }

    val window = (i - 25) until i
    val sums: List<BigInteger> = window.toList()
        .map { x ->
            window.toList()
                .filter { y -> y != x }
                .map { y -> this[x] + this[y] }
        }
        .flatten()
    return this[i] in sums
}

fun List<BigInteger>.contiguousSum(start: Int, targetSum: BigInteger): List<BigInteger> {
    return try {
        ((start + 2) .. this.size).toList()
            .map { end -> this.subList(start, end) }
            .first { sub -> sub.sumOf { it } == targetSum }
    } catch (e: NoSuchElementException) {
        emptyList()
    }
}

fun main() {
    val input = Day09::javaClass.javaClass.classLoader.getResource("day09.txt")?.readText() ?: ""
    val sequence = input.split("\n").map { it.toBigInteger() }

    val invalid = sequence[sequence.indices.first { !sequence.isValid(it) }]
    println(invalid)

    val subSequence = (1 until sequence.size).toList()
        .map { i -> sequence.contiguousSum(i, invalid) }
        .first { it.isNotEmpty() }
    val min = subSequence.minOrNull() ?: throw Exception()
    val max = subSequence.maxOrNull() ?: throw Exception()
    println(min + max)
}