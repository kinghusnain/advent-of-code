
fun List<Long>.cupGameTransform(): List<Long> {
    val currentCup = this[0]
    val pickedUp = this.slice(1..3)
    val newCups = (this.slice(0 until 1)
            + this.slice(4 until this.size))
        .toMutableList()
    var destination = currentCup - 1
    while (destination !in newCups) {
        destination = if (destination > 1) destination - 1 else 9
    }
    val destIdx = newCups.indexOf(destination)
    newCups.addAll(destIdx+1, pickedUp)
    newCups.add(newCups[0])
    newCups.removeAt(0)
    return newCups.toList()
}

class CupGameLL(initialCups: List<Long>) {
    data class Cup(val value: Long, var next: Cup?)
    private var current: Cup? = Cup(initialCups[0], null)
    private val cupWithLabel = mutableMapOf(initialCups[0] to current)

    init {
        var last = current
        for (n in initialCups.subList(1, initialCups.size)) {
            cupWithLabel[n] = Cup(n, null)
            last?.next = cupWithLabel[n]
            last = last?.next
        }
        last?.next = current
    }

    override fun toString(): String {
        val start = current
        var str = "${start?.value} "
        var cup = start?.next
        while (start?.value != cup?.value) {
            str += "${cup?.value} "
            cup = cup?.next
        }
        return str
    }

    fun playRound() {
        val removed = current?.next
        current?.next = removed?.next?.next?.next

        var destVal = current?.value!! - 1
        while (destVal in listOf(0,
                                  removed?.value,
                                  removed?.next?.value,
                                  removed?.next?.next?.value)) {
            destVal = if (destVal > 1) destVal - 1 else cupWithLabel.keys.maxOrNull()!!
        }
        val destination = cupWithLabel[destVal]!!

        removed?.next?.next?.next = destination.next
        destination.next = removed

        current = current!!.next
    }

    fun theAnswer(): Long {
        var cup1 = current
        while (cup1?.value != 1L) {
            cup1 = cup1?.next
        }
        return cup1.next!!.value * cup1.next!!.next!!.value
    }
}

fun main() {
    var cups = listOf(4L, 9L, 6L, 1L, 3L, 8L, 5L, 2L, 7L)
    for (n in 1..100) {
        cups = cups.cupGameTransform()
    }
    println(cups)

    val cupGame =  CupGameLL(listOf(4L, 9L, 6L, 1L, 3L, 8L, 5L, 2L, 7L))
    for (n in 1..100) {
        cupGame.playRound()
    }
    println(cupGame)

    val totalCups = 1000000L
    val totalRounds = 10000000L

    val manyCupsHandleIt = listOf(4L, 9L, 6L, 1L, 3L, 8L, 5L, 2L, 7L) + (10L..totalCups)
    val cupGame2 =  CupGameLL(manyCupsHandleIt.toMutableList())
    for (n in 1..totalRounds) {
        cupGame2.playRound()
    }
    println(cupGame2.theAnswer())
}