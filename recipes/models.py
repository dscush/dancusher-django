from django.db import models
from django.core.urlresolvers import reverse


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True, blank=True)
    serving_size = models.FloatField()
    unit = models.CharField(max_length=50)
    calories = models.FloatField()
    fat = models.FloatField()
    carbs = models.FloatField()
    fiber = models.FloatField()
    sugar = models.FloatField()
    protein = models.FloatField()
    is_vegan = models.BooleanField()
    source_recipe = models.OneToOneField("Recipe", on_delete=models.CASCADE, related_name='as_ingredient', null=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    name = models.CharField(max_length=200)
    description = models.CharField(max_length=200, null=True, blank=True)
    ingredients = models.ManyToManyField(Ingredient, through='RecipeIngredient')
    servings = models.FloatField()

    def get_absolute_url(self):
        return reverse('recipe_details', kwargs={'recipe_id':self.id})

    @property
    def is_vegan(self):
        for ingredient in self.ingredients.all():
            if not ingredient.is_vegan:
                return False
        return True

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE)
    count = models.FloatField()
