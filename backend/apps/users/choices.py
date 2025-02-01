from django.db import models
from django.utils.regex_helper import Choice


class BodyTypeChoice(models.TextChoices):
    Hatchback = 'Hatchback'
    Sedan = 'Sedan'
    Coupe = 'Coupe'
    Jeep = 'Jeep'
    Wagon = 'Wagon'
