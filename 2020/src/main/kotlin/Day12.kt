import kotlin.math.abs

class HMSDay12 {
    var xPos = 0
    var yPos = 0
    var facing = 90
    var xWaypoint = 10
    var yWaypoint = 1

    val go = mapOf(
        'N' to { dist: Int -> yPos += dist },
        'S' to { dist: Int -> yPos -= dist },
        'E' to { dist: Int -> xPos += dist },
        'W' to { dist: Int -> xPos -= dist },
        'L' to { degrees: Int -> facing = Math.floorMod(facing - degrees, 360) },
        'R' to { degrees: Int -> facing = Math.floorMod(facing + degrees, 360) },
        'F' to { dist: Int -> when (facing) {
            0 -> yPos += dist
            90 -> xPos += dist
            180 -> yPos -= dist
            270 -> xPos -= dist
            else -> throw Exception()
        }}
    )

    val moveWaypoint = mapOf(
        'N' to { dist: Int -> yWaypoint += dist },
        'S' to { dist: Int -> yWaypoint -= dist },
        'E' to { dist: Int -> xWaypoint += dist },
        'W' to { dist: Int -> xWaypoint -= dist },
        'L' to { degrees: Int -> when (degrees) {
            0 -> {}
            90 -> yWaypoint = xWaypoint.also { xWaypoint = -yWaypoint }
            180 -> {
                xWaypoint = -xWaypoint
                yWaypoint = -yWaypoint
            }
            270 -> xWaypoint = yWaypoint.also { yWaypoint = -xWaypoint }
            else -> throw Exception()
        }},
        'R' to { degrees: Int -> when (degrees) {
            0 -> {}
            90 -> xWaypoint = yWaypoint.also { yWaypoint = -xWaypoint }
            180 -> {
                xWaypoint = -xWaypoint
                yWaypoint = -yWaypoint
            }
            270 -> yWaypoint = xWaypoint.also { xWaypoint = -yWaypoint }
            else -> throw Exception()
        }},
        'F' to { dist: Int ->
            xPos += xWaypoint * dist
            yPos += yWaypoint * dist
        }
    )
}

fun main() {
    val input = HMSDay12::javaClass.javaClass.classLoader.getResource("day12.txt")?.readText() ?: ""
    val instructions = input.split("\n").map { Pair(it[0], it.substring(1).toInt()) }

    val ship1 = HMSDay12()
    instructions.forEach { (instr, dist) -> ship1.go[instr]?.invoke(dist) }
    println(abs(ship1.xPos) + abs(ship1.yPos))

    val ship2 = HMSDay12()
    instructions.forEach { (instr, dist) -> ship2.moveWaypoint[instr]?.invoke(dist) }
    println(abs(ship2.xPos) + abs(ship2.yPos))
}