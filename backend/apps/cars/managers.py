from django.db import models


class CarQuerySet(models.QuerySet):
    def less_than_year(self, year):
        return self.filter(year__lt=year)

    def only_audi(self):
        return self.filter(model='audi')

    def views_today(self):
        return self.filter()

    def filter_by_currency_price(self, currency, price_min=None, price_max=None):
        """
        Фільтрує автомобілі, де ціна в зазначеній валюті більша за price_min і менша за price_max.
        """
        queryset = self.filter(car_currency_prices__currency=currency)

        if price_min:
            queryset = queryset.filter(car_currency_prices__amount__gte=price_min)

        if price_max:
            queryset = queryset.filter(car_currency_prices__amount__lte=price_max)

        return queryset


class CarManager(models.Manager):
    def get_queryset(self):
        return CarQuerySet(self.model)

    def less_than_year(self, year):
        return self.get_queryset().less_than_year(year)

    def only_audi(self):
        return self.get_queryset().only_audi()

    def filter_by_currency_price(self, currency, price_min=None, price_max=None):
        return self.get_queryset().filter_by_currency_price(currency, price_min, price_max)
