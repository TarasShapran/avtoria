from datetime import datetime

from core.dataclasses.user_dataclass import User
from core.models import BaseModel
from core.services.s3_service import CarStorage

from django.contrib.auth import get_user_model
from django.core import validators as V
from django.db import models

from apps.auto_parks.models import AutoParkModel
from apps.car_dealership.models import CarDealership
from apps.cars.choices import BodyTypeChoice, CurrencyChoice
from apps.cars.managers import CarManager
from apps.cars.regex import CarRegex

UserModel: User = get_user_model()


class CarModel(BaseModel):
    class Meta:
        db_table = 'cars'

    brand = models.CharField(max_length=50, validators=[V.RegexValidator(*CarRegex.BRAND.value)])
    model = models.CharField(max_length=50, validators=[V.RegexValidator(*CarRegex.MODEL.value)])
    body_type = models.CharField(max_length=9, choices=BodyTypeChoice.choices)
    price = models.IntegerField(validators=[V.MinValueValidator(1), V.MaxValueValidator(100_000_000)])
    currency = models.CharField(max_length=3, choices=CurrencyChoice.choices, default=CurrencyChoice.UAH)
    year = models.IntegerField(validators=[V.MinValueValidator(1990), V.MaxValueValidator(datetime.now().year)])
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE, related_name='cars',null=True)
    dealership = models.ForeignKey(CarDealership, on_delete=models.CASCADE, related_name='cars', null=True)

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
