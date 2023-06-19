# Generated by Django 4.2.2 on 2023-06-19 13:34

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('crackerjacksapi', '0003_division_team_division'),
    ]

    operations = [
        migrations.AlterField(
            model_name='parkrating',
            name='rating',
            field=models.PositiveIntegerField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
