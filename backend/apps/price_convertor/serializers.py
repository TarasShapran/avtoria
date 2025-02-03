from rest_framework import serializers

from apps.price_convertor.models import ExchangeRateISOModel


class ExchangeRateISOSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExchangeRateISOModel
        fields = '__all__'
