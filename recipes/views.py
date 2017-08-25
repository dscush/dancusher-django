from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

from .models import Recipe, Ingredient

def index(request):
    recipe_list = Recipe.objects.all()
    context = {'recipe_list': recipe_list}
    return render(request, 'recipes/index.html', context)

def recipe_details(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    headers = ["Ingredient", "Amount", "Unit", "Calories", "Fat (g)", "Fat (%)", "Carbs (g)", "Carbs (%)", "Protien (g)", "Protein (%)"]
    ingredients = [[
        ingredient.ingredient.name,
        ingredient.count * ingredient.ingredient.serving_size,
        ingredient.ingredient.unit,
        round(ingredient.ingredient.calories * ingredient.count),
        ingredient.ingredient.fat * ingredient.count,
        str(round((100 * 9 * ingredient.ingredient.fat) / ingredient.ingredient.calories, 2)) + '%',
        ingredient.ingredient.carbs * ingredient.count,
        str(round((100 * 4 * ingredient.ingredient.carbs) / ingredient.ingredient.calories, 2)) + '%',
        ingredient.ingredient.protein * ingredient.count,
        str(round((100 * 4 * ingredient.ingredient.protein) / ingredient.ingredient.calories, 2)) + '%',
    ] for ingredient in recipe.recipeingredient_set.all()]
    total = [
        'Total',
        recipe.servings,
        'servings',
        sum([ingredient[3] for ingredient in ingredients]),
        sum([ingredient[4] for ingredient in ingredients]),
    ]
    total.append(str(round((100 * 9 * total[4]) / total[3], 2)) + '%')
    total.append(sum([ingredient[6] for ingredient in ingredients]))
    total.append(str(round((100 * 4 * total[6]) / total[3], 2)) + '%')
    total.append(sum([ingredient[8] for ingredient in ingredients]))
    total.append(str(round((100 * 4 * total[8]) / total[3], 2)) + '%')
    ingredients.append(total)
    ingredients.append([
        'Per Serving',
        1,
        'serving',
        round(total[3] / recipe.servings),
        round(total[4] / recipe.servings, 2),
        total[5],
        round(total[6] / recipe.servings, 2),
        total[7],
        round(total[8] / recipe.servings, 2),
        total[9],
    ])
    return render(request, 'recipes/recipe_details.html', {'recipe': recipe, 'ingredients': ingredients, 'headers': headers})

def ingredient_details(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
    headers = ["Amount", "Unit", "Calories", "Grams Fat", "Percent Fat", "Grams Protien", "Percent Protein"]
    ing = [
        ingredient.serving_size,
        ingredient.unit,
        ingredient.calories,
        ingredient.fat,
        str(round((100 * 9 * ingredient.fat) / ingredient.calories, 2)) + '%',
        ingredient.protein,
        str(round((100 * 4 * ingredient.protein) / ingredient.calories, 2)) + '%',
    ]
    return render(request, 'recipes/ingredient_details.html', {'ingredient': ingredient, 'ing': ing, 'headers': headers})
