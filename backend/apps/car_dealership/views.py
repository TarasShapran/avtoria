import logging

from core.permissions.user_permissions import (
    IsDealershipAdminManagerOrOwner,
    IsDealershipAdminOrOwner,
    IsDealershipOwner,
    IsDealershipOwnerOrReadOnly,
)
from drf_yasg.utils import swagger_auto_schema

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.utils.decorators import method_decorator

from rest_framework import status
from rest_framework.generics import (
    CreateAPIView,
    GenericAPIView,
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    get_object_or_404,
)
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework.response import Response

from apps.car_dealership.choices import DealershipRoleChoice
from apps.car_dealership.models import DealershipModel, DealershipUserModel
from apps.car_dealership.serializers import (
    AddAdminToDealershipSerializer,
    DealershipCarsSerializer,
    DealershipSerializer,
    DealershipUserSerializer,
)
from apps.cars.models import CarModel
from apps.cars.serializers import CarSerializer

logger = logging.getLogger(__name__)

UserModel = get_user_model()


class DealershipListCreateView(ListCreateAPIView):
    serializer_class = DealershipSerializer
    queryset = DealershipModel.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
        super().perform_create(serializer)


class DealershipRetrieveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    serializer_class = DealershipSerializer
    queryset = DealershipModel.objects.all()
    permission_classes = (IsDealershipOwnerOrReadOnly,)


class AddRoleToDealershipView(CreateAPIView):
    queryset = DealershipModel.objects.all()
    permission_classes = (IsDealershipOwner,)
    serializer_class = AddAdminToDealershipSerializer

    def create(self, request, *args, **kwargs):
        logger.info(self.get_object())
        dealership = self.get_object()
        serializer = self.get_serializer(data=request.data, context={'dealership': dealership})  # Передаємо в context
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class RetrieveUpdateDestroyRoleToDealershipView(RetrieveUpdateDestroyAPIView):
    queryset = DealershipUserModel.objects.select_related('dealership').all()
    permission_classes = (IsDealershipAdminOrOwner,)
    serializer_class = DealershipUserSerializer

    def _check_permissions(self, request, instance):
        request_user = request.user

        if instance.user == request_user:
            raise PermissionDenied("You can't change your own role")

        if instance.user == instance.dealership.owner:
            raise PermissionDenied("You can't change dealership's owner role")

        if instance.role == DealershipRoleChoice.Admin.value:
            raise PermissionDenied("You can't change administrator role")

    def perform_update(self, serializer):
        instance = self.get_object()
        self._check_permissions(self.request, instance)
        serializer.save()

    def perform_destroy(self, instance):
        self._check_permissions(self.request, instance)
        instance.delete()


class DealershipAddCarView(GenericAPIView):
    queryset = DealershipModel.objects.all()
    permission_classes = (IsDealershipAdminManagerOrOwner,)

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = CarSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        dealership = self.get_object()
        serializer.save(dealership=dealership)
        dealership_serializer = DealershipCarsSerializer(dealership)
        return Response(dealership_serializer.data, status.HTTP_201_CREATED)


class DealershipRetrieveUpdateDeleteCarView(RetrieveUpdateDestroyAPIView):
    queryset = CarModel.objects.select_related("dealership").all()
    serializer_class = CarSerializer
    permission_classes = (IsDealershipAdminManagerOrOwner,)

    def get_object(self):
        dealership_id = self.kwargs["dealership_id"]
        car_id = self.kwargs["car_id"]
        return get_object_or_404(CarModel, id=car_id, dealership_id=dealership_id)
