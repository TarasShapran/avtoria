# Generated by Django 5.1.5 on 2025-02-01 13:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_usermodel_is_premium_usermodel_role'),
    ]

    operations = [
        migrations.AlterField(
            model_name='usermodel',
            name='role',
            field=models.CharField(choices=[('Buyer', 'Buyer'), ('Seller', 'Seller'), ('Manager', 'Manager'), ('Admin', 'Admin')], default='Buyer', max_length=15),
        ),
    ]
