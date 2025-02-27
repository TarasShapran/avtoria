from django.core.cache import cache
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver

from .models import CarModel


@receiver([post_save, post_delete], sender=CarModel)
def invalidate_car_cache(sender, instance, **kwargs):
    print('Clearing the CarModel cache')
    cache.delete_pattern('*cars_list*')
