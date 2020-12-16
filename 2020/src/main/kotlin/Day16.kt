class Day16 {}

data class TicketField(val name: String,
                       val validValues: List<Int>,
                       val possiblePositions: MutableSet<Int>)

fun main() {
    val rulesInput = Day16::javaClass.javaClass.classLoader.getResource("day16-rules.txt")?.readText() ?: ""
    val validValues = rulesInput.split("\n")
        .map { """(\d+-\d+)""".toRegex().findAll(it).toList() }.flatten()
        .map { r -> r.value }
        .map { range ->
            val (min, max) = range.split("-", limit = 2).map { it.toInt() }
            return@map (min..max).toList()
        }
        .flatten()
        .toSet()
    val nearbyInput = Day16::javaClass.javaClass.classLoader.getResource("day16-nearby.txt")?.readText() ?: ""
    val nearbyValues = nearbyInput.split("\n")
        .map { it.split(",") }.flatten()
        .map { it.toInt() }
    val invalidValues = nearbyValues.filter { it !in validValues }
    val errorRate = invalidValues.sum()
    println(errorRate)

    val validTickets = nearbyInput.split("\n")
        .map { it.split(",").map { s -> s.toInt() } }
        .filter {
            for (v in it) {
                if (v !in validValues) return@filter false
            }
            return@filter true
        }
    val valuesForPosition = validTickets[0].indices
        .map { i -> validTickets.map { it[i] } }

    val ticketFields = rulesInput.split("\n")
        .mapNotNull { """([ a-z]+): (\d+)-(\d+) or (\d+)-(\d+)""".toRegex().matchEntire(it) }
        .map {
            val (name, min1, max1, min2, max2) = it.destructured
            val validValues1 = (min1.toInt() .. max1.toInt()).toList()
            val validValues2 = (min2.toInt() .. max2.toInt()).toList()
            return@map TicketField(
                name,
                validValues1 + validValues2,
                validTickets[0].indices.toMutableSet())
        }
    for (fieldIdx in ticketFields.indices) {
        for (pos in validTickets[0].indices) {
            var ruledOut = false
            for (v in valuesForPosition[pos]) {
                if (v !in ticketFields[fieldIdx].validValues) {
                    ruledOut = true
                }
            }
            if (ruledOut) {
                ticketFields[fieldIdx].possiblePositions.removeIf { it == pos }
            }
        }
    }
    while (ticketFields.filter { it.possiblePositions.size == 1 }.size < ticketFields.size) {
        ticketFields.filter { it.possiblePositions.size == 1 }.forEach {
            for (fieldIdx in ticketFields.indices) {
                if (it.name != ticketFields[fieldIdx].name) {
                    ticketFields[fieldIdx].possiblePositions.removeIf { p ->
                        p == it.possiblePositions.first()
                    }
                }
            }
        }
    }
    val myTicket = "223,139,211,131,113,197,151,193,127,53,89,167,227,79,163,199,191,83,137,149"
        .split(",")
        .map { it.toLong() }
    val theAnswer = ticketFields.filter { it.name.startsWith("departure") }
        .map { it.possiblePositions.first() }
        .map { myTicket[it] }
        .fold(1) { acc: Long, i: Long -> acc * i }
    println(theAnswer)
}