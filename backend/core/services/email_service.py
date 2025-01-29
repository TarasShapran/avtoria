import os

from configs.celery import app
from core.dataclasses.user_dataclass import User
from core.services.jwt_service import ActionToken, ActivateToken, JWTService, RecoverToken

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from apps.users.models import UserModel


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
    def send_test(cls):
        cls.__send_email('demchyshyn.v87@gmail.com', 'test.html', {}, 'Test Email')

    @classmethod
    def register(cls, user: User):
        token = JWTService.create_token(user, ActivateToken)
        url = f'http://localhost:3000/activate/{token}'
        cls.__send_email(
            user.email,
            'register.html',
            {'name': user.profile.name, 'url': url},
            'Register Email'
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

    @staticmethod
    @app.task
    def spam():
        for user in UserModel.objects.all():
            EmailService.__send_email(user.email, 'spam.html', {}, 'Spam')
