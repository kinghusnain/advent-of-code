import org.junit.jupiter.api.Test

class Day01Tests {
    private val day01 = Day01()

    @Test
    fun part1() {
        val sampleData = listOf(
            1721,
            979,
            366,
            299,
            675,
            1456
        )
        assert(day01.part1(sampleData) == 514579)
    }

    @Test
    fun part2() {
        val sampleData = listOf(
            1721,
            979,
            366,
            299,
            675,
            1456
        )
        assert(day01.part2(sampleData) == 241861950)
    }
}