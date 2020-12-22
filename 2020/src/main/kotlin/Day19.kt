sealed class MessageRule
data class ResolvedRule(val validMsgs: List<String>): MessageRule()
data class UnresolvedRule(val ruleSequences: List<List<Int>>): MessageRule()
typealias MessageRuleSet = MutableMap<Int, MessageRule>

fun MessageRuleSet.resolve(idx: Int) {
    val rule = this[idx]
    if (rule is UnresolvedRule) {
        val validMsgs = mutableSetOf<String>()
        rule.ruleSequences.forEach { seq ->
            var validSeqs = listOf("")
            seq.forEach { r ->
                this.resolve(r)
                val rr = this[r] as ResolvedRule
                validSeqs = validSeqs.combineWith(rr.validMsgs)
            }
            validMsgs.addAll(validSeqs)
            validMsgs.remove("")
        }
        this[idx] = ResolvedRule(validMsgs.toList())
    }
}

fun List<String>.combineWith(that: List<String>): List<String> =
    this.map { str -> that.map { str + it } }.flatten()

fun String.isEchoOf(shortStr: String): Boolean = when (this) {
    shortStr -> true
    else -> this.startsWith(shortStr) && this.substring(shortStr.length).isEchoOf(shortStr)
}

fun String.isValidByRule0(valid42s: List<String>, valid31s: List<String>): Boolean {
    for (i in 1 until this.length - 1) {
        val prefix = this.substring(0, i)
        val suffix = this.substring(i)
        if (prefix.isValidByRule8(valid42s) && suffix.isValidByRule11(valid42s, valid31s)) {
            return true
        }
    }
    return false
}

fun String.isValidByRule8(valid42s: List<String>): Boolean {
    if (this in valid42s) {
        return true
    } else {
        for (i in 1 until this.length - 1) {
            val prefix = this.substring(0, i)
            val suffix = this.substring(i)
            if (prefix in valid42s && suffix.isValidByRule8(valid42s)) {
                return true
            }
        }
        return false
    }
}

fun String.isValidByRule11(valid42s: List<String>, valid31s: List<String>): Boolean {
    for (i in 1 until this.length - 1) {
        val prefix = this.substring(0, i)
        val remainder = this.substring(i)
        if (prefix in valid42s) {
            if (remainder in valid31s) {
                return true
            }
            for (j in 1 until remainder.length - 1) {
                val middle = remainder.substring(0, j)
                val suffix = remainder.substring(j)
                if (middle.isValidByRule11(valid42s, valid31s) && suffix in valid31s) {
                    return true
                }
            }
        }
    }
    return false
}

fun main() {
    val input = MessageRule::javaClass.javaClass.classLoader.getResource("day19.txt")?.readText() ?: ""
    val (ruleInput, msgInput) = input.split("\n\n", limit = 2)

    val rules: MessageRuleSet = mutableMapOf()
    ruleInput.split("\n").forEach { str ->
        var (idx, reqs) = str.split(":", limit = 2)
        val i = idx.toInt()
        reqs = reqs.trim()
        if (reqs.startsWith('"')) {
            rules[i] = ResolvedRule(listOf(reqs[1].toString()))
        } else {
            val seqs = reqs.split("|")
                .map { seq ->
                    seq.trim().split(" ").map { it.toInt() }
                }
            rules[i] = UnresolvedRule(seqs)
        }
    }

    rules.resolve(0)
    val ruleZero = rules[0] as ResolvedRule
    val zeros = ruleZero.validMsgs

    val validMsgs1 = msgInput.split("\n").filter { it in zeros }
    println(validMsgs1.size)

    val fortyTwos = (rules[42] as ResolvedRule).validMsgs
    val thirtyOnes = (rules[31] as ResolvedRule).validMsgs

    val validMsgs2 = msgInput.split("\n").filter { it.isValidByRule0(fortyTwos, thirtyOnes) }
    println(validMsgs2.size)
}