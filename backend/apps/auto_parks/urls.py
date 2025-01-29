
from django.urls import path

from .views import AutoParkAddCarView, AutoParkListCreateAPIView

urlpatterns = [
    path('', AutoParkListCreateAPIView.as_view(), name='auto_park_list_create'),
    path('/<int:pk>/cars', AutoParkAddCarView.as_view(), name='auto_park_add_car'),
]