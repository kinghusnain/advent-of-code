import java.lang.Exception

interface PasswordRecord {
    fun isValid(): Boolean
}

fun List<PasswordRecord>.validRecords() = this.count { it.isValid() }

class PasswordRecord1(
    val policyMin: Int,
    val policyMax: Int,
    val policyChar: Char,
    val password: String
): PasswordRecord {
    fun policyCharCount() = password.count { it == policyChar }
    override fun isValid() = (policyMin <= policyCharCount()) && (policyCharCount() <= policyMax)
}

fun String.toPasswordRecord1(): PasswordRecord1 {
    val re = Regex("""(\d+)-(\d+)\s+(\w):\s*(\w+)""")
    val result = re.matchEntire(this) ?: throw Exception()
    val (min, max, ch, pass) = result.destructured
    return PasswordRecord1(min.toInt(), max.toInt(), ch[0], pass)
}

class PasswordRecord2(
    val position1: Int,
    val position2: Int,
    val policyChar: Char,
    val password: String
): PasswordRecord {
    override fun isValid() = (password[position1-1] == policyChar) xor (password[position2-1] == policyChar)
}

fun String.toPasswordRecord2(): PasswordRecord2 {
    val re = Regex("""(\d+)-(\d+)\s+(\w):\s*(\w+)""")
    val result = re.matchEntire(this) ?: throw Exception()
    val (p1, p2, ch, pass) = result.destructured
    return PasswordRecord2(p1.toInt(), p2.toInt(), ch[0], pass)
}

fun main() {
    val input = PasswordRecord1::javaClass.javaClass.classLoader.getResource("day02.txt")?.readText() ?: ""

    val part1data = input.split("\n").map { it.toPasswordRecord1() }
    val part1soln = part1data.validRecords()
    println(part1soln)

    val part2data = input.split("\n").map { it.toPasswordRecord2() }
    val part2soln = part2data.validRecords()
    println(part2soln)
}