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
    photos = CarPhotoSerializer(many=True, read_only=True)

    class Meta:
        model = CarModel
        # fields = '__all__'
        fields = ('id', 'model', 'body_type', 'price', 'year', 'photos', 'created_at', 'updated_at')
