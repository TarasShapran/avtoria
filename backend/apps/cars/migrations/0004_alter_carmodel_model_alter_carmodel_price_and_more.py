# Generated by Django 5.1.1 on 2024-09-30 17:10

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0003_carmodel_body_type'),
    ]

    operations = [
        migrations.AlterField(
            model_name='carmodel',
            name='model',
            field=models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[A-Z][a-zA-Z]{1,49}$', 'Model must consist fro first letter uppercase and only letters.')]),
        ),
        migrations.AlterField(
            model_name='carmodel',
            name='price',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(1000000)]),
        ),
        migrations.AlterField(
            model_name='carmodel',
            name='year',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1990), django.core.validators.MaxValueValidator(2024)]),
        ),
    ]
