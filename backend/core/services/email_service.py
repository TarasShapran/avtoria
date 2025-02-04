import os

from configs.celery import app
from core.dataclasses.user_dataclass import User
from core.services.jwt_service import ActionToken, ActivateToken, JWTService, RecoverToken

from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

UserModel: User = get_user_model()


class EmailService:
    @staticmethod
    @app.task
    def __send_email(to: str, template_name: str, context: dict, subject: str) -> None:
        template = get_template(template_name)
        html_content = template.render(context)
        msg = EmailMultiAlternatives(subject=subject, from_email=os.environ.get("EMAIL_HOST_USER"), to=[to])
        msg.attach_alternative(html_content, "text/html")
        msg.send()

    @classmethod
    def register(cls, user: User):
        token = JWTService.create_token(user, ActivateToken)
        url = f'http://localhost:3000/activate/{token}'
        cls.__send_email.delay(
            user.email,
            'register.html',
            {'name': user.profile.name, 'url': url},
            'Register Email'
        )

    @classmethod
    def validate_advertisement(cls, car):
        user = UserModel.objects.filter(is_staff=1).first()
        cls.__send_email.delay(
            user.email,
            'validate_advertisement.html',
            {'car_owner':car.user.email, 'car': car.id},
            'Validate advertisement Email'
        )

    @classmethod
    def recovery_password(cls, user: User):
        token = JWTService.create_token(user, RecoverToken)
        url = f'http://localhost:3000/recovery/{token}'
        cls.__send_email.delay(
            user.email,
            'recovery_password.html',
            {
                'name': user.profile.name,
                'url': url
            },
            'Recovery Password'
        )
        