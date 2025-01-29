import os
from uuid import uuid1

from core.dataclasses.user_dataclass import UserProfile


class PhotoService:
    @staticmethod
    def upload_avatar(instance: UserProfile, file: str) -> str:
        ext = file.split('.')[-1]
        return os.path.join(instance.surname, 'avatar', f'{uuid1()}.{ext}')

    @staticmethod
    def upload_car_photo(file: str, instance='cars') -> str:
        ext = file.split('.')[-1]
        return f'{uuid1()}.{ext}'
