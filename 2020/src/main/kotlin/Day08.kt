class GameConsole(private val program: Array<Instruction>) {
    data class Instruction(val operation: String, val argument: Int)
    var accumulator = 0
    var pc = 0
    var halted = false
    val ops = hashMapOf(
        "nop" to { },
        "acc" to { arg: Int -> this.accumulator += arg },
        "jmp" to { arg: Int -> this.pc += arg - 1 }
    )

    fun step() {
        if (this.pc < this.program.size) {
            val instruction = this.program[this.pc]
            this.ops[instruction.operation]?.invoke(instruction.argument)
            this.pc += 1
        } else {
            this.halted = true
        }
    }
}

fun String.toProgram() = this.split("\n")
    .map { it.split(" ") }
    .map { GameConsole.Instruction(it.first(), it.last().toInt()) }
    .toTypedArray()

fun main() {
    val input = GameConsole::javaClass.javaClass.classLoader.getResource("day08.txt")?.readText() ?: ""

    val program = input.toProgram()
    var console = GameConsole(program)
    var treadedGround = mutableSetOf<Int>()
    while (console.pc !in treadedGround && !console.halted) {
        treadedGround.add(console.pc)
        console.step()
    }
    println(console.accumulator)

    for (i in program.indices) {
        when (program[i].operation) {
            "nop" -> program[i] = GameConsole.Instruction("jmp", program[i].argument)
            "jmp" -> program[i] = GameConsole.Instruction("nop", program[i].argument)
            else -> continue
        }
        console = GameConsole(program)
        treadedGround = mutableSetOf()
        while (console.pc !in treadedGround && !console.halted) {
            treadedGround.add(console.pc)
            console.step()
        }
        if (console.halted) {
            println(console.accumulator)
            break
        }
        when (program[i].operation) {
            "nop" -> program[i] = GameConsole.Instruction("jmp", program[i].argument)
            "jmp" -> program[i] = GameConsole.Instruction("nop", program[i].argument)
        }
    }
}