from datetime import datetime

from core.dataclasses.user_dataclass import User
from core.models import BaseModel
from core.services.s3_service import CarStorage

from django.contrib.auth import get_user_model
from django.core import validators as V
from django.db import models

from apps.car_dealership.models import DealershipModel
from apps.cars.choices import BodyTypeChoice, CurrencyChoice, RegionChoice, StatusChoice
from apps.cars.managers import CarManager
from apps.cars.regex import CarRegex

UserModel: User = get_user_model()


class CarModel(BaseModel):
    class Meta:
        db_table = 'cars'

    brand = models.CharField(max_length=50, validators=[V.RegexValidator(*CarRegex.BRAND.value)])
    model = models.CharField(max_length=50, validators=[V.RegexValidator(*CarRegex.MODEL.value)])
    body_type = models.CharField(max_length=9, choices=BodyTypeChoice.choices)
    region = models.CharField(max_length=30, choices=RegionChoice.choices)
    price = models.IntegerField(validators=[V.MinValueValidator(1), V.MaxValueValidator(100_000_000)])
    description = models.CharField(max_length=500)
    currency = models.CharField(max_length=3, choices=CurrencyChoice.choices, default=CurrencyChoice.UAH)
    year = models.IntegerField(validators=[V.MinValueValidator(1990), V.MaxValueValidator(datetime.now().year)])
    status = models.CharField(max_length=15, choices=StatusChoice.choices, default=StatusChoice.Active)
    edit_attempts = models.IntegerField(default=0)
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='cars', null=True)
    dealership = models.ForeignKey(DealershipModel, on_delete=models.CASCADE, related_name='cars', null=True)

    objects = CarManager()


class CarImagesModel(BaseModel):
    class Meta:
        db_table = 'car_images'

    car = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='car_images')
    image = models.ImageField(storage=CarStorage())

    def save(self, *args, **kwargs):
        if car_dealership := self.car.dealership:
            self.image.storage.user_or_dealer = car_dealership.name
        else:
            self.image.storage.user_or_dealer = ''.join(str(self.car.user).split('@')[0])
        self.image.storage.car_model = self.car.model
        super(CarImagesModel, self).save(*args, **kwargs)

class CarCurrencyPriceModel(BaseModel):
    class Meta:
        db_table = 'car_currency_price'

    currency = models.CharField(max_length=3, choices=CurrencyChoice.choices)  # USD, EUR, UAH
    amount = models.DecimalField(max_digits=15, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    car = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='car_currency_prices')

class CarViewModel(models.Model):
    class Meta:
        db_table = 'car_view'

    car = models.ForeignKey(CarModel, related_name='views', on_delete=models.CASCADE)
    user = models.ForeignKey(UserModel, on_delete=models.SET_NULL, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

