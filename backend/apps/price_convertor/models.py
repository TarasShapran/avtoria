from core.models import BaseModel

from django.db import models


# Create your models here.
class ExchangeRateISOModel(BaseModel):
    class Meta:
        db_table = 'exchange_rate_iso'
        ordering = ['id']

    currencyCodeA = models.IntegerField()  # USD, EUR, UAH
    currencyCodeB = models.IntegerField()  # USD, EUR, UAH
    rateBuy = models.DecimalField(max_digits=15, decimal_places=5)
    rateSell = models.DecimalField(max_digits=15, decimal_places=5)