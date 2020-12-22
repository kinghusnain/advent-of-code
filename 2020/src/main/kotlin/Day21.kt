class Day21 {
}

data class FoodItem(val ingredients: List<String>, val allergens: List<String>)

fun main() {
    val input = Day21::javaClass.javaClass.classLoader.getResource("day21.txt")?.readText() ?: ""

    val foodItems = input.split("\n").map { foodItem ->
        val (ingredientList, allergenList) = foodItem.split("(")
        val ingredients = ingredientList.trim().split(" ")
        val allergens = allergenList.trim(' ', ')')
            .removePrefix("contains ").split(", ")
        FoodItem(ingredients, allergens)
    }
    val allIngredients = foodItems.map { it.ingredients }.flatten().toSet()
    val allAllergens = foodItems.map { it.allergens }.flatten().toSet()

    val candidatesForAllergen = mutableMapOf<String, MutableSet<String>>()
    for (allergen in allAllergens) {
        val allergicFood = foodItems.filter { allergen in it.allergens }
        candidatesForAllergen[allergen] = allergicFood.first().ingredients.toMutableSet()
        allergicFood.forEach { food ->
            allergicFood.first().ingredients.forEach { ingredient ->
                if (ingredient !in food.ingredients) {
                    candidatesForAllergen[allergen]?.remove(ingredient)
                }
            }
        }
    }

    while (allAllergens.map { candidatesForAllergen[it]!!.size }.sum() > allAllergens.size) {
        for (allergen in allAllergens) {
            if (candidatesForAllergen[allergen]?.size == 1) {
                val ingredient = candidatesForAllergen[allergen]!!.first()
                allAllergens.filter { it != allergen }.forEach {
                    candidatesForAllergen[it]!!.remove(ingredient)
                }
            }
        }
    }

    val allergenicIngredients = candidatesForAllergen.map { it.value.first() }.toSet()
    val hypoallergenicIngredients = allIngredients.filter { it !in allergenicIngredients }.toSet()

    val soln1 = foodItems.map { it.ingredients }.flatten().filter { it !in allergenicIngredients }.size
    println(soln1)

    val soln2 = candidatesForAllergen.toSortedMap().map { it.value.first() }.joinToString(",")
    println(soln2)
}