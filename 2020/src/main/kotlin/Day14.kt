class Day14 {}

fun Long.toBitString() = String.format("%9x", this)
    .map { when (it) {
        ' ' -> "0000"
        '0' -> "0000"
        '1' -> "0001"
        '2' -> "0010"
        '3' -> "0011"
        '4' -> "0100"
        '5' -> "0101"
        '6' -> "0110"
        '7' -> "0111"
        '8' -> "1000"
        '9' -> "1001"
        'a' -> "1010"
        'b' -> "1011"
        'c' -> "1100"
        'd' -> "1101"
        'e' -> "1110"
        'f' -> "1111"
        else -> throw Exception()
    } }
    .joinToString("")

typealias BitString = String
fun BitString.BStoLong(): Long = java.lang.Long.parseLong(this, 2)

fun BitString.mask(maskStr: String): BitString = maskStr.mapIndexed { i, c -> when (c) {
    '0' -> '0'
    '1' -> '1'
    else -> this[i]
} }.joinToString("")

fun BitString.mask2(maskStr: String): BitString = maskStr.mapIndexed { i, c -> when (c) {
    '1' -> '1'
    'X' -> 'X'
    else -> this[i]
} }.joinToString("")

fun String.floatingAddresses(): List<Long> {
    val i = this.indexOf('X')
    return if (i == -1) {
        listOf(this.BStoLong())
    } else {
        val zeroes = this.mapIndexed { idx, c -> if (i == idx) '0' else c }
            .joinToString("")
            .floatingAddresses()
        val ones = this.mapIndexed { idx, c -> if (i == idx) '1' else c }
            .joinToString("")
            .floatingAddresses()
        zeroes + ones
    }
}

fun main() {
    val input = Day14::javaClass.javaClass.classLoader.getResource("day14.txt")?.readText() ?: ""

    val mem = mutableMapOf<Long, Long>()
    var mask = ""
    input.split("\n").forEach {
        when {
            it.startsWith("mask") -> {
                mask = """[01X]+""".toRegex().find(it)?.value ?: throw Exception()
            }
            it.startsWith("mem") -> {
                val (addr, value) = """mem\[(\d+)]\s*=\s*(\d+)""".toRegex().matchEntire(it)?.destructured ?: throw Exception()
                val maskedValue = value.toLong().toBitString().mask(mask).BStoLong()
                mem[addr.toLong()] = maskedValue
            }
            else -> throw Exception()
        }
    }
    val sum = mem.toList().map { it.second }.reduce { acc, l -> acc + l }
    println(sum)

    val mem2 = mutableMapOf<Long, Long>()
    var mask2 = ""
    input.split("\n").forEach {
        when {
            it.startsWith("mask") -> {
                mask2 = """[01X]+""".toRegex().find(it)?.value ?: throw Exception()
            }
            it.startsWith("mem") -> {
                val (addr, value) = """mem\[(\d+)]\s*=\s*(\d+)""".toRegex().matchEntire(it)?.destructured ?: throw Exception()
                val maskedAddr = addr.toLong().toBitString().mask2(mask2)
                maskedAddr.floatingAddresses().forEach {
                    mem2[it] = value.toLong()
                }
            }
            else -> throw Exception()
        }
    }
    val sum2 = mem2.toList().map { it.second }.reduce { acc, l -> acc + l }
    println(sum2)
}