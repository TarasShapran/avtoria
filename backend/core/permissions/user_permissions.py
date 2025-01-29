from rest_framework.permissions import BasePermission, IsAdminUser


class IsSuperUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser and request.user.is_staff)


class IsOwnerPermissionOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True
        return obj.user == request.user
