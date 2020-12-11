import org.junit.jupiter.api.Test
import java.math.BigInteger

class Day10Tests {
    @Test
    fun p1() {
        val chain = CompleteAdapterChain(listOf(
            16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4
        ))
        assert(chain.ones == 7)
        assert(chain.threes == 5)

        val chain2 = CompleteAdapterChain(listOf(
            28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3
        ))
        assert(chain2.ones == 22)
        assert(chain2.threes == 10)
    }

    @Test
    fun p2() {
        val adapters1 = AdapterCollection(mutableListOf(
            16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4
        ))
        val paths1 = adapters1.numPaths()
        println(paths1)
        assert(paths1 == BigInteger.valueOf(8))

        val adapters2 = AdapterCollection(mutableListOf(
            28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3
        ))
        val paths2 = adapters2.numPaths()
        assert(paths2 == BigInteger.valueOf(19208))
    }
}