
from django_filters import rest_framework as filters

from apps.cars.choices import BodyTypeChoice
from apps.cars.models import CarModel


class CarFilter(filters.FilterSet):
    lt = filters.NumberFilter('year','lt')
    range = filters.RangeFilter('year') # range_min=2000&range_max=2010
    year_in = filters.BaseInFilter('year') # year_in=2000,2005,2010
    body_type = filters.ChoiceFilter('body_type', choices=BodyTypeChoice.choices)
    model_endwith = filters.CharFilter('model', 'endswith')
    order = filters.OrderingFilter(
        fields=(
            'id',
            'model',
            ('price', 'asd')
        )
    ) # order=-id


# CarModel.objects.filter(model__endswith=)