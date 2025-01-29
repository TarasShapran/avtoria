from datetime import datetime

from core.models import BaseModel
from core.services.s3_service import CarStorage

from django.core import validators as V
from django.db import models

from apps.auto_parks.models import AutoParkModel
from apps.cars.choices import BodyTypeChoice
from apps.cars.managers import CarManager
from apps.cars.regex import CarRegex
from apps.cars.services import upload_car_photo


class CarModel(BaseModel):
    class Meta:
        db_table = 'cars'

    model = models.CharField(max_length=50, validators=[V.RegexValidator(*CarRegex.MODEl.value)])
    body_type = models.CharField(max_length=9, choices=BodyTypeChoice.choices)
    price = models.IntegerField(validators=[V.MinValueValidator(1), V.MaxValueValidator(1_000_000)])
    year = models.IntegerField(validators=[V.MinValueValidator(1990), V.MaxValueValidator(datetime.now().year)])
    auto_park = models.ForeignKey(AutoParkModel, on_delete=models.CASCADE, related_name='cars')

    objects = CarManager()


class CarImagesModel(BaseModel):
    class Meta:
        db_table = 'car_images'

    car = models.ForeignKey(CarModel, on_delete=models.CASCADE, related_name='car_images')
    image = models.ImageField(storage=CarStorage())

    def save(self, *args, **kwargs):
        self.image.storage.car_model = self.car.model
        super(CarImagesModel, self).save(*args, **kwargs)
