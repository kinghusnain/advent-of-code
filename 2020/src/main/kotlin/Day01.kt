class Day01 {
    fun part1(entries: List<Int>): Int {
        for (m in entries) {
            for (n in entries) {
                if (m != n && n + m == 2020) {
                    return n * m
                }
            }
        }
        throw Exception()
    }

    fun part2(entries: List<Int>): Int {
        for (m in entries) {
            for (n in entries) {
                for (o in entries) {
                    if (m != n && n != o && m != o && n + m + o == 2020) {
                        return n * m * o
                    }
                }
            }
        }
        throw Exception()
    }
}

fun main() {
    val input = Day01::javaClass.javaClass.classLoader.getResource("day01.txt")?.readText()
    val part1data = input?.split("\n")?.map { it.toInt() } ?: listOf()
    val part1soln = Day01().part1(part1data)
    println(part1soln)
    val part2soln = Day01().part2(part1data)
    println(part2soln)
}