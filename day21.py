data = """..."""

test_data = """mxmxvkd kfcds sqjhc nhms (contains dairy, fish)
trh fvjkl sbzzf mxmxvkd (contains dairy)
sqjhc fvjkl (contains soy)
sqjhc mxmxvkd sbzzf (contains fish)"""

lines = test_data.split("\n")

# fill this dict and this list
allergen_to_poss_ingredients: dict[str, set[str]] = dict()
all_ingredients = []
for line in lines:
    line = line[:-1]  # trim ")" from (contains ...)
    ingredients, allergens = line.split(" (contains ")
    ingredients = ingredients.split(" ")
    allergens = allergens.split(", ")

    all_ingredients.extend(ingredients)
    for allergen in allergens:
        if allergen in allergen_to_poss_ingredients:
            allergen_to_poss_ingredients[allergen] &= set(ingredients)
        else:
            allergen_to_poss_ingredients[allergen] = set(ingredients)

# remove ingredients unique to one allergen
# from other allergen's candidate list
allergen_to_ingredient: dict[str, str] = dict()
while allergen_to_poss_ingredients:
    for allergen, ingredient_set in allergen_to_poss_ingredients.items():
        if len(ingredient_set) == 1:
            ingredient = ingredient_set.pop()
            del allergen_to_poss_ingredients[allergen]
            for other_ingredient_set in allergen_to_poss_ingredients.values():
                other_ingredient_set.discard(ingredient)
            allergen_to_ingredient[allergen] = ingredient
            break

allergen_ingredients = set(allergen_to_ingredient.values())

print(len([1 for ingredient in all_ingredients if ingredient not in allergen_ingredients]))

allergen_ingredients = sorted(allergen_to_ingredient.items())
print(",".join([x[1] for x in allergen_ingredients]))
