from django.conf.urls import url

from . import views


urlpatterns = [
    # ex: /recipes/
    url(r'^$', views.index, name='index'),
    # ex: /recipes/5/
    url(r'^(?P<recipe_id>[0-9]+)/$', views.recipe_details, name='recipe_details'),
    # ex: /recipes/ingredient/5/
    url(r'^ingredient/(?P<ingredient_id>[0-9]+)/$', views.ingredient_details, name='ingredient_details'),
    # ex: /recipes/5/duplicate/
    url(r'(?P<recipe_id>[0-9]+)/duplicate/$', views.duplicate_recipe, name='duplicate_recipe')
]
