from django.urls import path

from .views import AddPhotoByCarIdView, CarRetrieveUpdateDestroyView, CarsListCreateView, CarStatisticView

urlpatterns = [
    path('', CarsListCreateView.as_view(), name='cars_create_list'),
    path('/<int:pk>', CarRetrieveUpdateDestroyView.as_view(), name='cars_retrieve_update_destroy'),
    # path('/<int:pk>/photos', CarAddPhotosView.as_view(), name='cars_add_photos'),
    path('/<int:pk>/photo', AddPhotoByCarIdView.as_view(), name='cars_add_photo'),
    path('/<int:pk>/statistic', CarStatisticView.as_view(), name='cars_statistic'),

]
