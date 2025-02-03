from decimal import Decimal
from typing import List

from core.enums.currency_code import CurrencyCodeEnum
from core.services.currency_exchange_service import ExchangeRateService

from rest_framework import serializers

from apps.cars.models import CarCurrencyPriceModel, CarImagesModel, CarModel
from apps.price_convertor.models import ExchangeRateISOModel


class CarCurrencyPriceSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarCurrencyPriceModel
        fields = ('currency', 'amount',)


class CarPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImagesModel
        fields = ('image',)
        extra_kwargs = {
            'image': {
                'required': True
            }
        }


class CarSerializer(serializers.ModelSerializer):
    car_images = CarPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = CarModel
        fields = (
            'id', 'model', 'brand', 'currency', 'price', 'description', 'body_type', 'year', 'car_images', 'user',
            'created_at', 'updated_at')

    def save(self, **kwargs):
        super().save(**kwargs)
        if (base_price := self.instance.price) and (base_currency := self.instance.currency):
            ExchangeRateService.set_car_prices(self.instance, base_price, base_currency)

        return CarModel.objects.all().filter(id=self.instance.id)
