from enum import IntEnum

from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404, redirect

from .models import Recipe, Ingredient

class Macro(IntEnum):
    PROTEIN = 4
    CARB = 4
    FAT = 9

def index(request):
    recipe_list = Recipe.objects.all()
    ingredient_list = Ingredient.objects.all()
    context = {'recipe_list': recipe_list, 'ingredient_list': ingredient_list}
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
        _calc_calorie_percent(Macro.FAT, ingredient.ingredient.fat, ingredient.ingredient.calories),
        ingredient.ingredient.carbs * ingredient.count,
        _calc_calorie_percent(Macro.CARB, ingredient.ingredient.carbs, ingredient.ingredient.calories),
        ingredient.ingredient.protein * ingredient.count,
        _calc_calorie_percent(Macro.PROTEIN, ingredient.ingredient.protein, ingredient.ingredient.calories),
    ] for ingredient in recipe.recipeingredient_set.all()]
    total = [
        'Total',
        recipe.servings,
        'servings',
        sum([ingredient[3] for ingredient in ingredients]),
        sum([ingredient[4] for ingredient in ingredients]),
    ]
    total.append(_calc_calorie_percent(Macro.FAT, total[4], total[3]))
    total.append(sum([ingredient[6] for ingredient in ingredients]))
    total.append(_calc_calorie_percent(Macro.CARB, total[6], total[3]))
    total.append(sum([ingredient[8] for ingredient in ingredients]))
    total.append(_calc_calorie_percent(Macro.PROTEIN, total[8], total[3]))
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
    ingredients = map(
        lambda ingredient: map(
            lambda field: round(field, 3) if type(field) == float else field, ingredient
        ), ingredients
    )
    return render(request, 'recipes/recipe_details.html', {'recipe': recipe, 'ingredients': ingredients, 'headers': headers})

def ingredient_details(request, ingredient_id):
    ingredient = get_object_or_404(Ingredient, pk=ingredient_id)
    headers = ["Amount", "Unit", "Calories", "Fat (g)", "Fat (%)", "Carbs (g)", "Carbs (%)", "Protien (g)", "Protein (%)"]
    ing = [
        ingredient.serving_size,
        ingredient.unit,
        ingredient.calories,
        ingredient.fat,
        _calc_calorie_percent(Macro.FAT, ingredient.fat, ingredient.calories),
        ingredient.carbs,
        _calc_calorie_percent(Macro.CARB, ingredient.carbs, ingredient.calories),
        ingredient.protein,
        _calc_calorie_percent(Macro.PROTEIN, ingredient.protein, ingredient.calories),
    ]
    return render(request, 'recipes/ingredient_details.html', {'ingredient': ingredient, 'ing': ing, 'headers': headers})

def duplicate_recipe(request, recipe_id):
    recipe = Recipe.objects.get(id=recipe_id)
    ingredients = recipe.recipeingredient_set.all()
    recipe.pk = None
    recipe.save()
    recipe.recipeingredient_set.set(ingredients)
    recipe.save()
    return redirect(recipe)

def _calc_calorie_percent(macro_type, macro_grams, total_calories):
    if total_calories == 0:
        return '0'
    return str(round((100 * macro_type.value * macro_grams) / total_calories, 2)) + '%'
