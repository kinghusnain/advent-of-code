class Day06 {}

fun groupResponses(input: String) = input.split("\n\n")
    .map { it.filter { c -> c in 'a'..'z' } }
    .map { x -> x.toSet().toList() }

fun groupMemberResponses(input: String) = input.split("\n\n")
    .map {
        it.split("\n")
            .map { it.filter { c -> c in 'a'..'z' } }
            .map { x -> x.toSet().toList() }
    }

fun main() {
    val input = Day06::javaClass.javaClass.classLoader.getResource("day06.txt")?.readText() ?: ""

    val groupResponses = groupResponses(input)
    val affirmativeGroupResponses = groupResponses.fold(0) { count, res -> count + res.size}
    println(affirmativeGroupResponses)

    val groupMemberResponses = groupMemberResponses(input)
    val unanimousResponses = groupMemberResponses
        .map { it.reduce { l1, l2 -> (l1 intersect l2).toList() } }
        .fold(0) { count, l1 -> count + l1.size }
    println(unanimousResponses)
}