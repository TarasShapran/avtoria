from core.models import BaseModel

from django.contrib.auth import get_user_model
from django.db import models

from apps.car_dealership.choices import DealershipRoleChoice

User = get_user_model()


class DealershipModel(BaseModel):
    class Meta:
        db_table = 'dealerships'
    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="my_dealerships")

    def __str__(self):
        return self.name


class DealershipUserModel(BaseModel):
    class Meta:
        db_table = 'dealership_users'
        unique_together = ('user', 'dealership', 'role')

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="dealership_roles")
    dealership = models.ForeignKey(DealershipModel, on_delete=models.CASCADE, related_name="dealership_users")
    role = models.CharField(max_length=20, choices=DealershipRoleChoice.choices)

    def __str__(self):
        return f"{self.user} - {self.role} at {self.dealership}"
