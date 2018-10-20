# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2018-10-20 03:07
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0006_ingredient_is_vegan'),
    ]

    operations = [
        migrations.AddField(
            model_name='ingredient',
            name='source_recipe',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='as_ingredient', to='recipes.Recipe'),
        ),
    ]
