import logging

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from apps.car_dealership.choices import DealershipRoleChoice
from apps.car_dealership.models import DealershipModel, DealershipUserModel
from apps.cars.serializers import CarSerializer
from apps.users.serializers import UserSerializer, UserShortInfoSerializer

logger = logging.getLogger(__name__)

UserModel = get_user_model()


class DealershipUserSerializer(serializers.ModelSerializer):
    user = UserShortInfoSerializer(read_only=True)

    class Meta:
        model = DealershipUserModel
        fields = ('dealership', 'role', 'user')
        read_only_fields = ('user', 'dealership')
        validators = [
            UniqueTogetherValidator(
                queryset=DealershipUserModel.objects.all(),
                fields=['dealership', 'role', 'user'],
                message="Records: ('user', 'dealership', 'role') must be uniq"
            )
        ]


class DealershipSerializer(serializers.ModelSerializer):
    dealership_users = DealershipUserSerializer(many=True, read_only=True)
    cars = CarSerializer(many=True, read_only=True)

    class Meta:
        model = DealershipModel
        fields = ('id', 'name', 'owner', 'dealership_users', 'cars', 'created_at', 'updated_at')
        read_only_fields = ('owner', 'id')


class DealershipCarsSerializer(serializers.ModelSerializer):
    cars = CarSerializer(many=True, read_only=True)

    class Meta:
        model = DealershipModel
        fields = ('id', 'name', 'cars', 'created_at', 'updated_at')
        read_only_fields = ('id',)


class AddAdminToDealershipSerializer(serializers.ModelSerializer):
    dealership = DealershipSerializer(read_only=True)

    class Meta:
        model = DealershipUserModel
        fields = ['user', 'dealership', 'role']

    def validate(self, attrs):
        dealership = self.context.get('dealership')
        attrs['dealership'] = dealership

        if DealershipUserModel.objects.filter(user=attrs['user'], dealership=dealership, role=attrs['role']).exists():
            raise ValidationError({"non_field_errors": ["This user already has this role in this dealership."]})

        return attrs
