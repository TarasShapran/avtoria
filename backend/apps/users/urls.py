from django.urls import path

from .views import (
    AdminToUserView,
    TestEmailView,
    UserBanView,
    UserMeView,
    UsersListCreateView,
    UserToAdminView,
    UserUnBanView,
)

urlpatterns = [
    path('', UsersListCreateView.as_view(), name='users_list_create'),
    path('/me', UserMeView.as_view(), name='user_me'),
    path('/<int:pk>/ban', UserBanView.as_view(), name='user_ban' ),
    path('/<int:pk>/unban', UserUnBanView.as_view(), name='user_unban' ),
    path('/<int:pk>/to_admin', UserToAdminView.as_view(), name='user_to_admin' ),
    path('/<int:pk>/to_user', AdminToUserView.as_view(), name='admin_to_user' ),
    path('/test', TestEmailView.as_view(), name='test_email' ),
]
