from django.urls import path

from .views import (
    AddRoleToDealershipView,
    DealershipListCreateView,
    DealershipRetrieveUpdateDestroyView,
    RetrieveUpdateDestroyRoleToDealershipView,
)

urlpatterns = [
    path('', DealershipListCreateView.as_view(), name='dealership_create_list'),
    path('/<int:pk>', DealershipRetrieveUpdateDestroyView.as_view(), name='dealership_create_list'),
    path('/<int:pk>/managmentPersonal', RetrieveUpdateDestroyRoleToDealershipView.as_view(), name='dealership_create_list'),
    path('/<int:pk>/addAdmin', AddRoleToDealershipView.as_view(), name='add_admin_to_dealership'),
]
