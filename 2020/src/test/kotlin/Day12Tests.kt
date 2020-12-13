import org.junit.jupiter.api.Test
import kotlin.math.abs

class Day12Tests {
    @Test
    fun pt1() {
        val input = """F10
N3
F7
R90
F11"""
        val instructions = input.split("\n").map { Pair(it[0], it.substring(1).toInt()) }
        val ship = HMSDay12()
        instructions.forEach { (instr, dist) ->
            ship.go[instr]?.invoke(dist)
        }
        assert(abs(ship.xPos) + abs(ship.yPos) == 25)
    }

    @Test
    fun pt2() {
        val input = """F10
N3
F7
R90
F11"""
        val instructions = input.split("\n").map { Pair(it[0], it.substring(1).toInt()) }
        val ship = HMSDay12()
        instructions.forEach { (instr, dist) ->
            ship.moveWaypoint[instr]?.invoke(dist)
        }
        assert(abs(ship.xPos) + abs(ship.yPos) == 286)
    }
}