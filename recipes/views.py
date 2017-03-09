from django.http import HttpResponse, Http404
from django.shortcuts import render, get_object_or_404

from .models import Recipe, Ingredient

def index(request):
    recipe_list = Recipe.objects.all()
    context = {'recipe_list': recipe_list}
    return render(request, 'recipes/index.html', context)

def recipe_details(request, recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    ingredients = [[
        ingredient.ingredient.name,
        round(ingredient.ingredient.calories * ingredient.count),
        ingredient.ingredient.protein * ingredient.count,
        round((100 * 4 * ingredient.ingredient.protein) / ingredient.ingredient.calories, 2),
    ] for ingredient in recipe.recipeingredient_set.all()]
    total = [
        'Total',
        sum([ingredient[1] for ingredient in ingredients]),
        sum([ingredient[2] for ingredient in ingredients]),
    ]
    total.append(round((100 * 4 * total[2]) / total[1], 2))
    ingredients.append(total)
    ingredients.append(['Per Serving', round(total[1] / recipe.servings), round(total[2] / recipe.servings, 2), total[3]])
    return render(request, 'recipes/recipe_details.html', {'recipe': recipe, 'ingredients': ingredients})

def ingredient_details(request, ingredient_id):
    response = "You're looking at ingredient %s."
    return HttpResponse(response % ingredient_id)
