import logging

from rest_framework.permissions import BasePermission, IsAdminUser

from apps.car_dealership.choices import DealershipRoleChoice
from apps.car_dealership.models import DealershipModel, DealershipUserModel
from apps.cars.models import CarModel

logger = logging.getLogger()


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser and request.user.is_staff)


class IsOwnerPermissionOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return obj.user == request.user

class IsPremiumUser(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.user == request.user and request.user.is_premium


class IsDealershipOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, DealershipUserModel):
            return obj.dealership.owner == request.user
        elif isinstance(obj, DealershipModel):
            return obj.owner == request.user


class IsDealershipOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if isinstance(obj, DealershipUserModel):
            return obj.dealership.owner == request.user
        elif isinstance(obj, DealershipModel):
            return obj.owner == request.user


class IsDealershipAdminOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.dealership.owner == request.user:
            return True

        if DealershipUserModel.objects.filter(
                user=request.user,
                dealership=obj.dealership,
                role=DealershipRoleChoice.Admin
        ).exists():
            return True

        return False


class IsDealershipAdminManagerOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, CarModel):
            obj = obj.dealership

        if obj.owner == request.user:
            return True

        if DealershipUserModel.objects.filter(
                user=request.user,
                dealership=obj,
                role__in=(DealershipRoleChoice.Admin.value, DealershipRoleChoice.Manager.value)
        ).exists():
            return True

        return False
