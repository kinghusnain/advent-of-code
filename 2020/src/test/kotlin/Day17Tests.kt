import org.junit.jupiter.api.Test

class Day17Tests {
    @Test
    fun pt1() {
        val pd0 = PocketDimension3D()
        pd0.load2D(".#.\n..#\n###")
        assert(pd0.activeCount() == 5)
        val pd1 = pd0.next()
        for (y in 1..3) {
            for (x in 0..2) {
                if (pd1.isActive(x, y, -1)) {
                    print('#')
                } else {
                    print('.')
                }
            }
            println()
        }
        val pd6 = pd1.next().next().next().next().next()
        assert(pd6.activeCount() == 112)
    }

    @Test
    fun pt2() {
        val pd0 = PocketDimension4D()
        pd0.setState(1,1,1,1, true)
        assert(pd0.isActive(1,1,1,1))
        pd0.setState(1,1,1,1, false)
        assert(!pd0.isActive(1,1,1,1))
        pd0.load2D(".#.\n..#\n###")
        assert(pd0.activeCount() == 5)
        val pd6 = pd0.next().next().next().next().next().next()
        assert(pd6.activeCount() == 848)
    }
}