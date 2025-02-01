# Generated by Django 5.1.5 on 2025-02-01 13:10

import core.services.s3_service

import django.core.validators
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('car_dealership', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CarModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('brand', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[A-Z][a-zA-Z]{1,49}$', 'Model must consist for first letter uppercase and only letters.')])),
                ('model', models.CharField(max_length=50, validators=[django.core.validators.RegexValidator('^[A-Z][a-zA-Z0-9 ]{0,49}$', 'Model must start with an uppercase letter and contain only letters, numbers, and spaces.')])),
                ('body_type', models.CharField(choices=[('Hatchback', 'Hatchback'), ('Sedan', 'Sedan'), ('Coupe', 'Coupe'), ('Jeep', 'Jeep'), ('Wagon', 'Wagon')], max_length=9)),
                ('price', models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(100000000)])),
                ('currency', models.CharField(choices=[('USD', 'Usd'), ('EUR', 'Eur'), ('UAH', 'Uah')], default='UAH', max_length=3)),
                ('year', models.IntegerField(validators=[django.core.validators.MinValueValidator(1990), django.core.validators.MaxValueValidator(2025)])),
                ('car_dealership', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cars', to='car_dealership.cardealership')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='cars', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'cars',
            },
        ),
        migrations.CreateModel(
            name='CarImagesModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('image', models.ImageField(storage=core.services.s3_service.CarStorage(), upload_to='')),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car_images', to='cars.carmodel')),
            ],
            options={
                'db_table': 'car_images',
            },
        ),
    ]
