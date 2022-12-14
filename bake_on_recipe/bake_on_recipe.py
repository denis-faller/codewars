def cakes(recipe, available):
    availableProductsOnRecipe = {}
    for product in available:
        if (product in available) and (product in recipe):
            availableProductsOnRecipe[product] = int(available[product] / recipe[product])
    for product in recipe:
        if (product not in available):
            availableProductsOnRecipe[product] = 0

    return min(availableProductsOnRecipe.values())