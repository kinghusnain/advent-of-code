import kotlin.math.max
import kotlin.math.min

class CrabCombat(private val p1deck: MutableList<Int>,
                 private val p2deck: MutableList<Int>) {
    private fun playRound() {
        val p1card = p1deck.removeAt(0)
        val p2card = p2deck.removeAt(0)
        val winner = if (p1card > p2card) p1deck else p2deck
        winner.add(max(p1card, p2card))
        winner.add(min(p1card, p2card))
    }

    fun playGame() {
        while (p1deck.isNotEmpty() && p2deck.isNotEmpty()) {
            playRound()
        }
    }

    private fun score(deck: MutableList<Int>) = deck.reversed()
        .mapIndexed { i, card -> card * (i + 1) }
        .sum()

    fun winnerScore() = score(p1deck) + score(p2deck)
}

class RecursiveCombat(private val p1deck: MutableList<Int>,
                      private val p2deck: MutableList<Int>) {
    private var winner: Int? = null
    private val roundHistory = mutableListOf<String>()

    private fun playRound() {
        val deckStamp = deckStamp()
        if (deckStamp in roundHistory) {
            winner = 1
            return
        }
        roundHistory.add(deckStamp)

        val p1card = p1deck.removeAt(0)
        val p2card = p2deck.removeAt(0)
        if (p1deck.size >= p1card && p2deck.size >= p2card) {
            val p1deckCopy = p1deck.subList(0, p1card).toMutableList()
            val p2deckCopy = p2deck.subList(0, p2card).toMutableList()
            val subGame = RecursiveCombat(p1deckCopy, p2deckCopy)
            val winner = subGame.playGame()
            if (winner == 1) {
                p1deck.add(p1card)
                p1deck.add(p2card)
            } else {
                p2deck.add(p2card)
                p2deck.add(p1card)
            }
        } else {
            val winningDeck = if (p1card > p2card) p1deck else p2deck
            winningDeck.add(max(p1card, p2card))
            winningDeck.add(min(p1card, p2card))
        }

        if (p1deck.isEmpty()) {
            winner = 2
        } else if (p2deck.isEmpty()) {
            winner = 1
        }
    }

    fun playGame(): Int {
        while (winner == null) {
            playRound()
        }
        return winner!!
    }

    private fun score(deck: MutableList<Int>) = deck.reversed()
        .mapIndexed { i, card -> card * (i + 1) }
        .sum()

    fun winnerScore(): Int? = when (winner) {
        1 -> score(p1deck)
        2 -> score(p2deck)
        else -> null
    }

    private fun deckStamp(): String {
        val p1 = p1deck.joinToString { it.toString() }
        val p2 = p2deck.joinToString { it.toString() }
        return p1 + p2
    }
}

fun main() {
    val input = CrabCombat::javaClass.javaClass.classLoader.getResource("day22.txt")?.readText() ?: ""
    val (p1deck, p2deck) = input.split("\n\n").map { d ->
        d.split("\n")
            .filter { !it.startsWith("Player") }
            .map {
                it.toInt()
            }
    }

    val game = CrabCombat(p1deck.toMutableList(), p2deck.toMutableList())
    game.playGame()
    println(game.winnerScore())

    val game2 = RecursiveCombat(p1deck.toMutableList(), p2deck.toMutableList())
    game2.playGame()
    println(game2.winnerScore())
}