from django.urls import path

from .views import AddPhotoByCarIdView, CarAddPhotosView, CarRetrieveUpdateDestroyView, CarsListView

urlpatterns = [
    path('', CarsListView.as_view(), name='cars_create_list'),
    path('/<int:pk>', CarRetrieveUpdateDestroyView.as_view(), name='cars_retrieve_update_destroy'),
    # path('/<int:pk>/photos', CarAddPhotosView.as_view(), name='cars_add_photos'),
    path('/<int:pk>/photo', AddPhotoByCarIdView.as_view(), name='cars_add_photo'),
]
