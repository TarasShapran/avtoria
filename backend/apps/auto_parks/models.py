from core.models import BaseModel

from django.db import models


class AutoParkModel(BaseModel):
    class Meta:
        db_table = 'auto_parks'

    name = models.CharField(max_length=20)
