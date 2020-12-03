import org.junit.jupiter.api.Test

class Day03Tests {

    @Test
    fun test() {
        val treeMap = """..##.......
#...#...#..
.#....#..#.
..#.#...#.#
.#...##..#.
..#.##.....
.#.#.#....#
.#........#
#.##...#...
#...##....#
.#..#...#.#""".toTreeMap()

        assert(treeMap.height() == 11)

        assert(treeMap.treeAt(0,1))
        assert(treeMap.treeAt(1,2))
        assert(treeMap.treeAt(2,3))
        assert(!treeMap.treeAt(3,4))

        val collisions = treeMap.numTreeStrikes(3, 1)
        assert(collisions == 7)
    }
}