from core.services.photo_service import PhotoService
from storages.backends.s3boto3 import S3Boto3Storage

CAR_LOCATION = 'car_images'
AVATAR_STORAGE = 'UploadFiles.storage_backends.CarImages'


class CarStorage(S3Boto3Storage):
    location = CAR_LOCATION
    default_acl = 'public-read'
    file_overwrite = False


    def _normalize_name(self, name):
        name = PhotoService.upload_car_photo(file=name)
        return super()._normalize_name(name)

    def get_available_name(self, name, max_length=None):
        car_model = getattr(self, 'car_model', 'default_car')
        user_or_dealer = getattr(self, 'user_or_dealer', 'default_user')
        self.location = f'{CAR_LOCATION}/{user_or_dealer}/{car_model}'
        name = f'{self.location}/{name}'
        return super().get_available_name(name, max_length)
