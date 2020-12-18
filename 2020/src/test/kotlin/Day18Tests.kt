import org.junit.jupiter.api.Test

class Day18Tests {
    @Test
    fun pt1() {
        assert(Expression("1 + 2 * 3 + 4 * 5 + 6").eval() == 71L)
        assert(Expression("1 + (2 * 3) + (4 * (5 + 6))").eval() == 51L)
        assert(Expression("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2").eval() == 13632L)
    }

    @Test
    fun pt2() {
        assert(ExpressionV2("1 + 2 * 3 + 4 * 5 + 6").eval() == 231L)
        assert(ExpressionV2("2 * 3 + (4 * 5)").eval() == 46L)
        assert(ExpressionV2("5 + (8 * 3 + 9 + 3 * 4 * 3)").eval() == 1445L)
    }
}