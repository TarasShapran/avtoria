from django.db import models
from django.utils.regex_helper import Choice


class BodyTypeChoice(models.TextChoices):
    Hatchback = 'Hatchback'
    Sedan = 'Sedan'
    Coupe = 'Coupe'
    Jeep = 'Jeep'
    Wagon = 'Wagon'


class CurrencyChoice(models.TextChoices):
    USD = 'USD'
    EUR = 'EUR'
    UAH = 'UAH'

class StatusChoice(models.TextChoices):
    Pending = 'Pending'
    Active = 'Active'
    Inactive = 'Inactive'
    NeedReview = 'NeedReview'
