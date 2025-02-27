import logging
import time
from datetime import timedelta

from core.permissions.user_permissions import IsOwnerPermissionOrReadOnly, IsPremiumUser
from core.services.email_service import EmailService

from django.core.exceptions import PermissionDenied
from django.db.models.aggregates import Avg
from django.utils.decorators import method_decorator
from django.utils.timezone import now
from django.views.decorators.cache import cache_page

from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView, ListCreateAPIView, RetrieveAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.cars.choices import CurrencyChoice, StatusChoice
from apps.cars.filters import CarFilter
from apps.cars.models import CarModel
from apps.cars.serializers import CarPhotoSerializer, CarSerializer, CarViewSerializer

logger = logging.getLogger(__name__)


class CarsListCreateView(ListCreateAPIView):
    """
    get:
        Get cars
    post:
        create car
    """
    serializer_class = CarSerializer
    queryset = CarModel.objects.filter(status=StatusChoice.Active.value).all()
    filterset_class = CarFilter
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        time.sleep(5)
        return super().get_queryset()

    @method_decorator(cache_page(60 * 60, key_prefix='cars_list'))
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):

        user = request.user
        if not user.is_premium:
            car_count = CarModel.objects.filter(user=user).count()
            if car_count >= 1:
                raise PermissionDenied("You need to buy premium to add more than one car")

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        car = serializer.save(user=user)
        if serializer.profanity_errors:
            car.status = StatusChoice.Pending.value
            car.save()

            return Response(
                {
                    "detail": "Your listing contains prohibited words and needs to be edited.",
                    "status": "draft",
                    "errors": serializer.errors,
                    "data": CarSerializer(car).data
                },
                status=status.HTTP_206_PARTIAL_CONTENT
            )

        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)


class CarRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    """
    get:
        Get car by id
    put:
        Full Update car by id
    patch:
        Partial Update car by id
    delete:
        Delete car by id
    """
    queryset = CarModel.objects.exclude(status=StatusChoice.Inactive.value).all()
    serializer_class = CarSerializer
    permission_classes = (IsOwnerPermissionOrReadOnly,)
    filterset_class = CarFilter

    def get(self, request, *args, **kwargs):
        car = self.get_object()
        if (car.user and request.user != car.user) or (car.dealership and car.dealership != request.user):
            data = {
                'car': car.id,
                'user': request.user.id if request.user else None
            }
            serializer = CarViewSerializer(data=data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
        return super().get(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):

        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)

        edit_attempts = instance.edit_attempts

        if (edit_attempts <= 2 and serializer.profanity_errors) or (
                instance.status == StatusChoice.Pending.value and edit_attempts <= 2):
            edit_attempts += 1
            instance.edit_attempts = edit_attempts
            instance.save()
            return Response(
                {
                    "detail": f"Your listing contains prohibited words and needs to be edited. You have {4 - edit_attempts}",
                    "status": "draft",
                    "errors": serializer.errors,
                    "data": CarSerializer(instance).data
                },
                status=status.HTTP_206_PARTIAL_CONTENT
            )
        elif edit_attempts >= 3:
            instance.status = StatusChoice.NeedReview.value
            instance.save()
            EmailService.validate_advertisement(instance)
            raise PermissionDenied(
                "You have exceeded the maximum number of edit attempts. The listing is now under review.")

        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            instance._prefetched_objects_cache = {}

        return super().update(request, *args, **kwargs)


class AddPhotoByCarIdView(GenericAPIView):
    queryset = CarModel.objects.prefetch_related('car_images').all()
    permission_classes = (IsOwnerPermissionOrReadOnly,)

    def post(self, request, *args, **kwargs):
        car = self.get_object()
        images = request.data.getlist('image', None)
        if not images:
            raise serializers.ValidationError('image: this field is required')

        for image in images:
            data = {'image': image}
            photo_serializer = CarPhotoSerializer(data=data)
            photo_serializer.is_valid(raise_exception=True)
            photo_serializer.save(car=car)
        car_serializer = CarSerializer(car)
        return Response(car_serializer.data, status.HTTP_201_CREATED)


class CarStatisticView(RetrieveAPIView):
    queryset = CarModel.objects.prefetch_related('views', 'car_currency_prices').all()
    permission_classes = (IsPremiumUser,)
    serializer_class = CarSerializer

    def retrieve(self, request, *args, **kwargs):
        car: CarModel = self.get_object()
        serializer = self.get_serializer(car)

        today = now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)

        total_views = car.views.count()
        views_today = car.views.filter(created_at__date=today).count()
        views_this_week = car.views.filter(created_at__date__gte=week_ago).count()
        views_this_month = car.views.filter(created_at__date__gte=month_ago).count()

        average_price_in_region = (
            CarModel.objects
            .prefetch_related('car_currency_prices')
            .filter(region=car.region, car_currency_prices__currency=CurrencyChoice.USD.value)
            .aggregate(average_price=Avg('car_currency_prices__amount'))['average_price']
        )

        average_price_in_ukraine = (
            CarModel.objects
            .prefetch_related('car_currency_prices')
            .filter(car_currency_prices__currency=CurrencyChoice.USD.value).exclude(status=StatusChoice.Inactive)
            .aggregate(average_price=Avg('car_currency_prices__amount'))['average_price']
        )

        data = {
            "car": serializer.data,
            "statistics": {
                "total_views": total_views,
                "views_today": views_today,
                "views_this_week": views_this_week,
                "views_this_month": views_this_month,
                "average_price_in_region": round(average_price_in_region, 2) if average_price_in_region else None,
                "average_price_in_ukraine": round(average_price_in_ukraine, 2) if average_price_in_ukraine else None,
            }
        }
        return Response(data, status=status.HTTP_200_OK)
