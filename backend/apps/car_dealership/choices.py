from django.db import models
from django.utils.regex_helper import Choice


class DealershipRoleChoice(models.TextChoices):
    Admin = 'Admin'
    Manager = 'Manager'
    Sales = 'Sales'
    Mechanic = 'Mechanic'
