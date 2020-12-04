import java.lang.NumberFormatException

class Day04 {}

fun String.toPassportDataMap() =
    Regex("""([a-z]+):(\S+)""").findAll(this)
    .map { result ->
        val (field, value) = result.destructured
        Pair(field, value)
    }.toMap()

fun Map<String, String>.hasValidPassportFields() =
        "byr" in this
                && "iyr" in this
                && "eyr" in this
                && "hgt" in this
                && "hcl" in this
                && "ecl" in this
                && "pid" in this

fun Map<String, String>.hasValidPassportData() =
        this["byr"].inIntRange(1920, 2002)
                && this["iyr"].inIntRange(2010, 2020)
                && this["eyr"].inIntRange(2020, 2030)
                && this["hgt"].isValidHeight()
                && this["hcl"]?.let { Regex("""#[0-9a-z]{6}""").matches(it) } == true
                && this["ecl"] in setOf("amb", "blu", "brn", "gry", "grn", "hzl", "oth")
                && this["pid"]?.let { Regex("""\d{9}""").matches(it) } == true

fun String?.inIntRange(min: Int, max: Int) =
    this != null && this.toInt() in min..max

fun String?.isValidHeight(): Boolean {
    if (this == null) return false
    return try {
        val units = this.reversed().substring(0, 2).reversed()
        val value = this.reversed().substring(2).reversed().toInt()
        when (units) {
            "cm" -> value in 150..193
            "in" -> value in 59..76
            else -> false
        }
    } catch (e: NumberFormatException) {
        false
    }
}

fun main() {
    val validExamples = """ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
""".split("\n\n")
        .map { passportStr -> passportStr.toPassportDataMap() }
        .filter { entry -> entry.hasValidPassportFields() }
        .size
    println(validExamples)

    val input = Day04::javaClass.javaClass.classLoader.getResource("day04.txt")?.readText() ?: ""

    val numWithReqFields = input.split("\n\n")
        .map { passportStr -> passportStr.toPassportDataMap() }
        .filter { entry -> entry.hasValidPassportFields() }
        .size
    println(numWithReqFields)

    val numValid = input.split("\n\n")
        .map { passportStr -> passportStr.toPassportDataMap() }
        .filter { entry -> entry.hasValidPassportData() }
        .size
    println(numValid)
}