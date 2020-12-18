class Expression(private var expression: String) {
    private val exprStack = mutableListOf<Long>()

    fun eval(): Long {
        evalNextExpr()
        return exprStack.removeAt(exprStack.lastIndex)
    }

    private fun evalNextExpr() {
        evalNextTerm()
        while (expression.isNotEmpty() && expression.first() in setOf('+', '*')) {
            when (expression.first()) {
                '+' -> {
                    expression = expression.substring(1).trim()
                    evalNextTerm()
                    val t1 = exprStack.removeAt(exprStack.lastIndex)
                    val t2 = exprStack.removeAt(exprStack.lastIndex)
                    exprStack.add(t1 + t2)
                }
                '*' -> {
                    expression = expression.substring(1).trim()
                    evalNextTerm()
                    val t1 = exprStack.removeAt(exprStack.lastIndex)
                    val t2 = exprStack.removeAt(exprStack.lastIndex)
                    exprStack.add(t1 * t2)
                }
            }
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

fun main() {
    val input = Expression::javaClass.javaClass.classLoader.getResource("day18.txt")?.readText() ?: ""

    val pt1sum = input.split("\n").map { Expression(it).eval() }.sum()
    println(pt1sum)

    val pt2sum = input.split("\n").map { ExpressionV2(it).eval() }.sum()
    println(pt2sum)
}