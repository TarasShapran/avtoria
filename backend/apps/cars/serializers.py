from rest_framework import serializers

from apps.cars.models import CarImagesModel, CarModel


class CarPhotoSerializer(serializers.ModelSerializer):
    class Meta:
        model = CarImagesModel
        fields = ('image',)
        extra_kwargs = {
            'image': {
                'required': True
            }
        }


class CarSerializer(serializers.ModelSerializer):
    car_images = CarPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = CarModel
        fields = ('id', 'model','brand', 'body_type', 'price', 'year', 'car_images', 'user', 'created_at', 'updated_at')
