import collections
import datetime
import logging
from decimal import Decimal
from typing import List

import requests
from configs.celery import app
from core.enums.currency_code import CurrencyCodeEnum

from apps.cars.models import CarCurrencyPriceModel, CarModel
from apps.price_convertor.models import ExchangeRateISOModel
from apps.price_convertor.serializers import ExchangeRateISOSerializer

logger = logging.getLogger(__name__)


class ExchangeRateService:
    MONOBANC_API_URL = 'https://api.monobank.ua/bank/currency'

    @staticmethod
    @app.task
    def __get_exchange_rates_from_monobank():
        response = requests.get(ExchangeRateService.MONOBANC_API_URL)
        if response.status_code == 200:
            return response.json()
        return []

    @staticmethod
    @app.task
    def update_exchange_rates_mono():
        exchange_rates = ExchangeRateService.__get_exchange_rates_from_monobank()

        for rate_data in exchange_rates:
            if rate_data['currencyCodeA'] not in [840, 978]:
                continue
            currencyCodeA = rate_data['currencyCodeA']
            currencyCodeB = rate_data['currencyCodeB']
            existing_rate = ExchangeRateISOModel.objects.filter(
                currencyCodeA=currencyCodeA,
                currencyCodeB=currencyCodeB).first()

            if existing_rate:
                serializer = ExchangeRateISOSerializer(existing_rate, data=rate_data)
            else:
                serializer = ExchangeRateISOSerializer(data=rate_data)

            if serializer.is_valid(raise_exception=True):
                serializer.save()

    @staticmethod
    @app.task
    def _calculate_price(car, base_price, base_currency, currency_rates):
        if not currency_rates:
            currency_rates: List[ExchangeRateISOModel] = ExchangeRateISOModel.objects.all()

        from apps.cars.serializers import CarCurrencyPriceSerializer
        currency_rates_map = dict()

        for currency_rate in currency_rates:
            currency_rates_map[(currency_rate.currencyCodeA, currency_rate.currencyCodeB)] = currency_rate.rateSell
            currency_rates_map[(currency_rate.currencyCodeB, currency_rate.currencyCodeA)] = currency_rate.rateBuy

        logger.info(car)
        logger.info(base_price)
        logger.info(base_currency)
        logger.info(currency_rates_map)
        for currency_code in CurrencyCodeEnum:
            iso_currency, currency = currency_code.code, currency_code.currency
            exchange_rate = currency_rates_map.get((int(iso_currency), CurrencyCodeEnum[base_currency].code))
            converted_amount = None

            if currency.upper() == base_currency:
                converted_amount = base_price
                exchange_rate = True

            if not exchange_rate:
                continue

            if currency.upper() != base_currency and base_currency == CurrencyCodeEnum.EUR.currency:
                converted_amount = base_price * Decimal(exchange_rate)
            elif currency.upper() != base_currency and base_currency == CurrencyCodeEnum.UAH.currency:
                converted_amount = base_price / Decimal(exchange_rate)
            elif currency.upper() != base_currency and base_currency == CurrencyCodeEnum.USD.currency:
                if currency.upper() == CurrencyCodeEnum.UAH.currency:
                    converted_amount = base_price * Decimal(exchange_rate)
                else:
                    converted_amount = base_price / Decimal(exchange_rate)

            if not converted_amount:
                continue
            data = {
                'currency': currency.upper(),
                'amount': round(converted_amount, 2)
            }
            serializer = CarCurrencyPriceSerializer(data=data)
            serializer.is_valid(raise_exception=True)

            car_currency_price = CarCurrencyPriceModel.objects.filter(car=car,
                                                                      currency=currency.upper()).first()
            if car_currency_price:
                serializer.update(car_currency_price, serializer.validated_data)
                logger.info(f"Updated price for {car.brand} in {currency}: {converted_amount}")
            else:
                serializer.save(car=car)
                logger.info(f"Created new price for {car.brand} in {currency}: {converted_amount}")

    @staticmethod
    @app.task
    def update_car_prices():
        logger.info(f"Start updating at {datetime.datetime.now()}")
        currency_rates_map = dict()
        cars = CarModel.objects.all()
        currency_rates: List[ExchangeRateISOModel] = ExchangeRateISOModel.objects.all()
        for currency_rate in currency_rates:
            currency_rates_map[(currency_rate.currencyCodeA, currency_rate.currencyCodeB)] = currency_rate.rateSell
            currency_rates_map[(currency_rate.currencyCodeB, currency_rate.currencyCodeA)] = currency_rate.rateBuy

        for car in cars:
            base_currency = car.currency
            base_price = car.price

            ExchangeRateService._calculate_price(car, base_price, base_currency, currency_rates)

        logger.info(f"Finished updating at {datetime.datetime.now()}")

    @classmethod
    def set_car_prices(cls, car, base_price, base_currency):
        logger.info(f"Start updating at {datetime.datetime.now()}")
        ExchangeRateService._calculate_price(car, base_price, base_currency, currency_rates=None)
