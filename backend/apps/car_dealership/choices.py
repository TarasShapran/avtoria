from django.db import models
from django.utils.regex_helper import Choice


class UserRoleChoice(models.TextChoices):
    buyer = 'Buyer'
    seller = 'Seller'
    manager = 'Manager'
    admin = 'Admin'
    dealer_admin = 'DealerAdmin'
    dealer_manager = 'DealerManager'
