from django.urls import path

from .views import (
    AddRoleToDealershipView,
    DealershipAddCarView,
    DealershipListCreateView,
    DealershipRetrieveUpdateDeleteCarView,
    DealershipRetrieveUpdateDestroyView,
    RetrieveUpdateDestroyRoleToDealershipView,
)

urlpatterns = [
    path('', DealershipListCreateView.as_view(), name='dealership_create_list'),
    path('/<int:pk>', DealershipRetrieveUpdateDestroyView.as_view(), name='dealership_retrieve_upd_del'),
    path('/<int:pk>/managmentPersonal', RetrieveUpdateDestroyRoleToDealershipView.as_view(),
         name='dealership_create_list'),
    path('/<int:pk>/addAdmin', AddRoleToDealershipView.as_view(), name='dealership_add_admin'),
    path('/<int:pk>/cars', DealershipAddCarView.as_view(), name='dealership_add_car'),
    path('/<int:dealership_id>/cars/<int:car_id>',
         DealershipRetrieveUpdateDeleteCarView.as_view(),
         name='manage-car'),
]
