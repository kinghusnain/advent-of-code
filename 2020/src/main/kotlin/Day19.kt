sealed class MessageRule
data class CharRule(val char: Char): MessageRule()
data class SequenceRule(val ruleSequences: List<List<Int>>): MessageRule()
typealias RuleSet = MutableMap<Int, MessageRule>

fun RuleSet.satisfiesRule(ruleIdx: Int, string: String) =
    this.match(ruleIdx, string) == ""

fun RuleSet.match(ruleIdx: Int, string: String): String? {
    if (string == "") return null
    val rule = this[ruleIdx]
    return when {
        (rule is CharRule) -> {
            if (string[0] == rule.char) string.substring(1) else null
        }
        (rule is SequenceRule) -> {
            rule.ruleSequences.forEach { seq ->
                var theRest: String? = string
                for (r in seq) {
                    if (theRest == null) {
                        break
                    }
                    theRest = this.match(r, theRest)
                    print("")
                }
                if (theRest != null) {
                    return theRest
                }
            }
            null
        }
        else -> null
    }
}

fun main() {
    val input = MessageRule::javaClass.javaClass.classLoader.getResource("day19.txt")?.readText() ?: ""
    val (ruleInput, msgInput) = input.split("\n\n", limit = 2)

    val rules: RuleSet = mutableMapOf()
    ruleInput.split("\n").forEach { str ->
        var (idx, reqs) = str.split(":", limit = 2)
        val i = idx.toInt()
        reqs = reqs.trim()
        if (reqs.startsWith('"')) {
            rules[i] = CharRule(reqs[1])
        } else {
            val seqs = reqs.split("|")
                .map { seq ->
                    seq.trim().split(" ").map { it.toInt() }
                }
            rules[i] = SequenceRule(seqs)
        }
    }

    val validMsgs1 = msgInput.split("\n").filter { rules.satisfiesRule(0, it) }
    println(validMsgs1.size)
}