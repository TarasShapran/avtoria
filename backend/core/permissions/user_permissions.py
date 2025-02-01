import logging

from rest_framework.permissions import BasePermission, IsAdminUser

from apps.car_dealership.choices import DealershipRoleChoice
from apps.car_dealership.models import CarDealership, DealershipUser

logger = logging.getLogger()


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser and request.user.is_staff)


class IsOwnerPermissionOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return obj.user == request.user


class IsDealershipOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if isinstance(obj, DealershipUser):
            return obj.dealership.owner == request.user
        elif isinstance(obj, CarDealership):
            return obj.owner == request.user

class IsDealershipOwnerOrReadOnly(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        if isinstance(obj, DealershipUser):
            return obj.dealership.owner == request.user
        elif isinstance(obj, CarDealership):
            return obj.owner == request.user


class IsDealershipAdminOrOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        if obj.dealership.owner == request.user:
            return True

        if DealershipUser.objects.filter(
                user=request.user,
                dealership=obj.dealership,
                role=DealershipRoleChoice.Admin
        ).exists():
            return True

        return False
