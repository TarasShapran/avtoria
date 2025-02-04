import logging

from core.exceptions.validation_exception import ProfanityValidationError
from core.services.currency_exchange_service import ExchangeRateService
from core.utils.profanity_filter import CustomProfanity

from django.core.exceptions import ValidationError

from rest_framework import serializers
from rest_framework.fields import empty

from apps.cars.choices import StatusChoice
from apps.cars.models import CarCurrencyPriceModel, CarImagesModel, CarModel

logger = logging.getLogger(__name__)

profanity_checker = CustomProfanity()


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

    def __init__(self, instance=None, data=empty, **kwargs):
        super().__init__(instance, data, **kwargs)
        self.profanity_errors = None

    def validate(self, attrs):
        errors = {}
        for field, data in attrs.items():
            if isinstance(data, (int, float)):
                continue
            if profanity_checker.contains_profanity(data):
                errors[
                    field] = f"{field} field contains prohibited words. Your text is: {profanity_checker.censor(data)}"
                attrs[field] = profanity_checker.censor(data)

        if errors:
            self.profanity_errors = errors

        return super().validate(attrs)

    def save(self, **kwargs):
        super().save(**kwargs)
        if (base_price := self.instance.price) and (base_currency := self.instance.currency):
            ExchangeRateService.set_car_prices(self.instance, base_price, base_currency)

        return self.instance
