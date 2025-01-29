from core.services.email_service import EmailService
from drf_yasg.utils import swagger_auto_schema

from django.contrib.auth import get_user_model

from rest_framework import serializers, status
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from apps.users.serializers import UserSerializer

UserModel = get_user_model()


class UsersListCreateView(ListCreateAPIView):
    queryset = UserModel.objects.select_related('profile').all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class UserMeView(GenericAPIView):
    serializer_class = UserSerializer
    queryset = UserModel.objects.select_related('profile').all()
    permission_classes = (IsAuthenticated,)

    def get(self, *args, **kwargs):
        user = self.request.user
        serializer = UserSerializer(user)
        return Response(serializer.data, status.HTTP_200_OK)


class UserBanView(GenericAPIView):
    queryset = UserModel.objects.all()

    def get_queryset(self):
        return super().get_queryset().exclude(id=self.request.user.id)

    def patch(self, *args, **kwargs):
        user = self.get_object()
        if user.is_active:
            user.is_active = False
            user.save()
        serializer = UserSerializer(user)

        return Response(serializer.data, status.HTTP_200_OK)


class ErrorSerializer(serializers.Serializer):
    details = serializers.CharField()


class UserUnBanView(GenericAPIView):
    queryset = UserModel.objects.all()

    # serializer_class = UserSerializer

    def get_serializer(self, *args, **kwargs):
        pass

    def get_queryset(self):
        return super().get_queryset().exclude(id=self.request.user.id)

    @swagger_auto_schema(responses={status.HTTP_200_OK: UserSerializer, status.HTTP_400_BAD_REQUEST: ErrorSerializer})
    def patch(self, *args, **kwargs):
        user = self.get_object()
        if not user.is_active:
            user.is_active = True
            user.save()
        serializer = UserSerializer(user)

        return Response(serializer.data, status.HTTP_200_OK)


class UserToAdminView(GenericAPIView):
    queryset = UserModel.objects.all()

    def get_queryset(self):
        return super().get_queryset().exclude(id=self.request.user.id)

    def patch(self, *args, **kwargs):
        user = self.get_object()
        if not user.is_staff:
            user.is_staff = True
            user.save()
        serializer = UserSerializer(user)

        return Response(serializer.data, status.HTTP_200_OK)


class AdminToUserView(GenericAPIView):
    queryset = UserModel.objects.all()

    def get_queryset(self):
        return super().get_queryset().exclude(id=self.request.user.id)

    def patch(self, *args, **kwargs):
        user = self.get_object()
        if user.is_staff:
            user.is_staff = False
            user.save()
        serializer = UserSerializer(user)

        return Response(serializer.data, status.HTTP_200_OK)


class TestEmailView(GenericAPIView):
    permission_classes = (AllowAny,)

    def get_serializer(self, *args, **kwargs):
        return None

    def get(self, *args, **kwargs):
        EmailService.send_test()

        return Response(status=status.HTTP_200_OK)
