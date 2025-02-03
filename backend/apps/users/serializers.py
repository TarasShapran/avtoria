from core.enums.regex_enum import RegEx
from core.services.email_service import EmailService
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from django.contrib.auth import get_user_model
from django.core import validators as V
from django.db.transaction import atomic

from rest_framework import serializers

from apps.users.models import ProfileModel

UserModel = get_user_model()


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileModel
        fields = ('id', 'name', 'surname', 'birth_day', 'phone_number', 'get_age', 'created_at', 'updated_at')


class ShortUsersInfo(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = (
            'id',
            'email'
        )


class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer()
    password = serializers.CharField(max_length=100, min_length=8, write_only=True, validators=[
        V.RegexValidator(*RegEx.PASSWORD.value)
    ])

    class Meta:
        model = UserModel
        fields = (
            'id',
            'email',
            'password',
            'is_active',
            'is_staff',
            'is_superuser',
            'last_login',
            'created_at',
            'updated_at',
            'profile'
        )

        read_only_fields = (
            'id', 'is_active', 'is_staff', 'is_superuser', 'last_login', 'created_at', 'updated_at')
        extra_kwargs = {
            'password': {
                'write_only': True,
            }
        }

    @atomic
    def create(self, validated_data: dict):
        profile = validated_data.pop('profile')
        profile = ProfileModel.objects.create(**profile)
        user = UserModel.objects.create_user(profile=profile, **validated_data)
        EmailService.register(user)
        return user


class LogoutUserSerializer(serializers.Serializer):
    refresh_token = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs.get('refresh_token')
        return attrs

    def save(self, **kwargs):
        try:
            token = RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail('Token expired')
