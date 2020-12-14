fun main() {
    val input = "13,x,x,41,x,x,x,x,x,x,x,x,x,997,x,x,x,x,x,x,x,23,x,x,x,x,x,x,x,x,x,x,19,x,x,x,x,x,x,x,x,x,29,x,619,x,x,x,x,x,37,x,x,x,x,x,x,x,x,x,x,17"

    val earliestDeparture = 1000390
    val operatingBuses = input.split(",").filter { it != "x" }.map { it.toInt() }
    val earliestBus = operatingBuses.map { busNum ->
        var t = 0
        while (t < earliestDeparture) t += busNum
        return@map Pair(busNum, t)
    }.minByOrNull { it.second } ?: throw Exception()
    val (busNum, departure) = earliestBus
    val waitTime = departure - earliestDeparture
    println(busNum * waitTime)
}