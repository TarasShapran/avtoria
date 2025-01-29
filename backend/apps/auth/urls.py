from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from django.urls import path

from .views import ActivateUserView, RecoveryPasswordRequestView, RecoveryPasswordView, SocketTokenView

urlpatterns = [
    path('', TokenObtainPairView.as_view(), name='auth_login'),
    path('/refresh', TokenRefreshView.as_view(), name='auth_refresh'),
    path('/activate/<str:token>', ActivateUserView.as_view(), name='auth_activate'),
    path('/recovery', RecoveryPasswordRequestView.as_view(), name='auth_recovery_password_request'),
    path('/recovery/<str:token>', RecoveryPasswordView.as_view(), name='auth_recovery_password'),
    path('/socket', SocketTokenView.as_view(), name='auth_socket_token'),
]
