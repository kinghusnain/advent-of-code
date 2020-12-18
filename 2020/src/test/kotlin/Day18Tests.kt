import org.junit.jupiter.api.Test

class Day18Tests {
    @Test
    fun testGetTrailingExpression() {
        val (head, tail) = getTrailingExpression("1 + 2 * 3 + 4 * 5 + 6")
        assert(head == "1 + 2 * 3 + 4 * 5 + ")
        assert(tail == "6")

        val (head2, tail2) = getTrailingExpression("1 + (2 * 3) + (4 * (5 + 6))")
        assert(head2 == "1 + (2 * 3) + ")
        assert(tail2 == "4 * (5 + 6)")
    }

    @Test
    fun testGetTrailingOperator() {
        val (head, tail) = getTrailingOperator("1 + 2 * 3 + 4 * 5 + ")
        assert(head == "1 + 2 * 3 + 4 * 5 ")
        assert(tail == "+")

        val (head2, tail2) = getTrailingOperator("1 + (2 * 3) + ")
        assert(head2 == "1 + (2 * 3) ")
        assert(tail2 == "+")
    }

    @Test
    fun pt1() {
        val ex1 = eval("1 + 2 * 3 + 4 * 5 + 6")
        assert(ex1 == 71L)
//        val ex6 = eval("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2")
//        assert(ex1 == 13632L)
    }

    @Test
    fun pt2() {
        assert(ExpressionV2("1 + 2 * 3 + 4 * 5 + 6").eval() == 231L)
        assert(ExpressionV2("2 * 3 + (4 * 5)").eval() == 46L)
        assert(ExpressionV2("5 + (8 * 3 + 9 + 3 * 4 * 3)").eval() == 1445L)
    }
}