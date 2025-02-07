# Generated by Django 5.1.5 on 2025-02-03 11:38

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cars', '0003_carmodel_description_carmodel_status'),
    ]

    operations = [
        migrations.CreateModel(
            name='CarCurrencyPriceModel',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('currency', models.CharField(choices=[('USD', 'Usd'), ('EUR', 'Eur'), ('UAH', 'Uah')], max_length=3)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=15)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('car', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='car_currency_prices', to='cars.carmodel')),
            ],
            options={
                'db_table': 'car_currency_price',
            },
        ),
    ]
