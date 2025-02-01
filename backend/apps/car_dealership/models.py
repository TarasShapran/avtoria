from core.models import BaseModel

from django.contrib.auth import get_user_model
from django.db import models

from apps.car_dealership.choices import DealershipRoleChoice

User = get_user_model()


class CarDealership(BaseModel):
    class Meta:
        db_table = 'car_dealership'
    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_dealerships")

    def __str__(self):
        return self.name


class DealershipUser(BaseModel):
    class Meta:
        db_table = 'car_dealership_user'
        unique_together = ('user', 'dealership', 'role')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dealership_roles")
    dealership = models.ForeignKey(CarDealership, on_delete=models.CASCADE, related_name="dealership_users")
    role = models.CharField(max_length=20, choices=DealershipRoleChoice.choices)

    def __str__(self):
        return f"{self.user} - {self.role} at {self.dealership}"
