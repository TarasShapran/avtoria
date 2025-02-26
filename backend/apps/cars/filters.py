from django_filters import rest_framework as filters

from apps.cars.choices import BodyTypeChoice, CurrencyChoice
from apps.cars.models import CarModel


class CarFilter(filters.FilterSet):
    lt = filters.NumberFilter('year', 'lt')
    range = filters.RangeFilter('year')
    year_in = filters.BaseInFilter('year')
    body_type = filters.ChoiceFilter('body_type', choices=BodyTypeChoice.choices)
    model_endwith = filters.CharFilter('model', 'endswith')
    currency = filters.ChoiceFilter(field_name='car_currency_prices__currency', choices=CurrencyChoice.choices)
    price_min = filters.NumberFilter(field_name='car_currency_prices__amount', lookup_expr='gte')
    price_max = filters.NumberFilter(field_name='car_currency_prices__amount', lookup_expr='lte')

    order = filters.OrderingFilter(
        fields=(
            'id',
            'model',
            'price'
        )
    )
