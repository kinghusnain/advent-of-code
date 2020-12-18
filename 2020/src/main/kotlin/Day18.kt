class Day18 {
}

class ExpressionV2(private var expression: String) {
    private val exprStack = mutableListOf<Long>()

    fun eval(): Long {
        evalNextExpr()
        return exprStack.removeAt(exprStack.lastIndex)
    }

    private fun evalNextExpr() {
        evalNextFactor()
        while (expression.isNotEmpty() && expression.first() == '*') {
            expression = expression.substring(1).trim()
            evalNextFactor()
            val t1 = exprStack.removeAt(exprStack.lastIndex)
            val t2 = exprStack.removeAt(exprStack.lastIndex)
            exprStack.add(t1 * t2)
        }
    }

    private fun evalNextFactor() {
        evalNextTerm()
        while (expression.isNotEmpty() && expression.first() == '+') {
            expression = expression.substring(1).trim()
            evalNextTerm()
            val t1 = exprStack.removeAt(exprStack.lastIndex)
            val t2 = exprStack.removeAt(exprStack.lastIndex)
            exprStack.add(t1 + t2)
        }
    }

    private fun evalNextTerm() {
        when {
            expression.first() in '0'..'9' -> {
                val num = expression.takeWhile { it in '0'..'9' }
                expression = expression.substring(num.length).trim()
                exprStack.add(num.toLong())
            }
            expression.first() == '(' -> {
                expression = expression.substring(1).trim()
                evalNextExpr()
                expression = expression.substring(1).trim()  // ')'
            }
        }
    }
}

fun eval(expression: String): Long {
    return try {
        expression.toLong()
    } catch (e: NumberFormatException) {
        val (head, tailExpr) = getTrailingExpression(expression)
        val (headExpr, operator) = getTrailingOperator(head)
        when (operator) {
            "+" -> eval(headExpr) + eval(tailExpr)
            "*" -> eval(headExpr) * eval(tailExpr)
            "" -> eval(tailExpr)
            else -> throw Exception()
        }
    }
}

fun getTrailingExpression(expression: String): Pair<String, String> {
    val expression = expression.trim()
    return when {
        expression.last() in '0'..'9' -> {
            val tail = expression.takeLastWhile { it in '0'..'9' }
            val head = expression.substring(0, expression.length - tail.length)
            Pair(head, tail)
        }
        expression.last() == ')' -> {
            var unclosed = 1
            var i = expression.lastIndex - 1
            while (unclosed > 0) {
                when (expression[i]) {
                    '(' -> unclosed -= 1
                    ')' -> unclosed += 1
                    else -> {}
                }
                i -= 1
            }
            val tail = expression.substring(i + 2, expression.length - 1)
            val head = expression.substring(0, i + 1)
            Pair(head, tail)
        }
        else -> throw Exception()
    }
}

fun getTrailingOperator(exprFrag: String): Pair<String, String> {
    val exprFrag = exprFrag.trim()
    return when {
        exprFrag == "" -> Pair("", "")
        exprFrag.last() in setOf('*', '+') -> Pair(exprFrag.substring(0, exprFrag.length - 1),
                                                   exprFrag.substring(exprFrag.length - 1))
        else -> throw Exception()
    }
}

fun main() {
    val input = Day18::javaClass.javaClass.classLoader.getResource("day18.txt")?.readText() ?: ""

    val pt1sum = input.split("\n").map { eval(it) }.sum()
    println(pt1sum)

    val pt2sum = input.split("\n").map { ExpressionV2(it).eval() }.sum()
    println(pt2sum)
}