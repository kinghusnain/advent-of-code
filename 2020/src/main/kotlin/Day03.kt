class TreeMap(private val map: Array<BooleanArray>) {
    fun height() = map.size
    fun treeAt(x: Int, y: Int) = map[y][x % (map[y].size)]
    fun numTreeStrikes(deltaX: Int, deltaY: Int): Int {
        var x = 0
        var y = 0
        var collisions = 0
        while (y < this.height() - 1) {
            x += deltaX
            y += deltaY
            if (this.treeAt(x, y)) {
                collisions += 1
            }
        }
        return collisions
    }
}

fun String.toTreeMap() = TreeMap(
    this.split("\n").map { row ->
        row.map { c ->
            c == '#'
        }.toBooleanArray()
    }.toTypedArray()
)

fun main() {
    val input = TreeMap::javaClass.javaClass.classLoader.getResource("day03.txt")?.readText() ?: ""
    val treeMap = input.toTreeMap()

    val collisions = treeMap.numTreeStrikes(3,1)
    println(collisions)

    var product = 1.toBigInteger()
    product *= treeMap.numTreeStrikes(1, 1).toBigInteger()
    product *= treeMap.numTreeStrikes(3, 1).toBigInteger()
    product *= treeMap.numTreeStrikes(5, 1).toBigInteger()
    product *= treeMap.numTreeStrikes(7, 1).toBigInteger()
    product *= treeMap.numTreeStrikes(1, 2).toBigInteger()
    println(product)
}