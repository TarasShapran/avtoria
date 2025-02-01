import logging

from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator

from apps.car_dealership.choices import DealershipRoleChoice
from apps.car_dealership.models import CarDealership, DealershipUser
from apps.users.serializers import ShortUsersInfo, UserSerializer

logger = logging.getLogger(__name__)

UserModel = get_user_model()


class DealershipUserSerializer(serializers.ModelSerializer):
    user = ShortUsersInfo(read_only=True)

    class Meta:
        model = DealershipUser
        fields = ('dealership', 'role', 'user')
        read_only_fields = ('user', 'dealership')
        validators = [
            UniqueTogetherValidator(
                queryset=DealershipUser.objects.all(),
                fields=['dealership', 'role', 'user'],
                message="Records: ('user', 'dealership', 'role') must be uniq"
            )
        ]


class DealershipSerializer(serializers.ModelSerializer):
    dealership_users = DealershipUserSerializer(many=True, read_only=True)

    class Meta:
        model = CarDealership
        fields = ('id', 'name', 'dealership_users', 'owner', 'created_at', 'updated_at')
        read_only_fields = ('owner', 'id')


class AddAdminToDealershipSerializer(serializers.ModelSerializer):
    dealership = DealershipSerializer(read_only=True)

    class Meta:
        model = DealershipUser
        fields = ['user', 'dealership', 'role']

    def validate(self, attrs):
        dealership = self.context.get('dealership')
        attrs['dealership'] = dealership

        if DealershipUser.objects.filter(user=attrs['user'], dealership=dealership, role=attrs['role']).exists():
            raise ValidationError({"non_field_errors": ["This user already has this role in this dealership."]})

        return attrs
