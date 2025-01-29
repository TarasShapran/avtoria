from rest_framework import status
from rest_framework.generics import GenericAPIView, ListCreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from apps.auto_parks.models import AutoParkModel
from apps.auto_parks.serializers import AutoParkSerializer
from apps.cars.serializers import CarSerializer


class AutoParkListCreateAPIView(ListCreateAPIView):
    serializer_class = AutoParkSerializer
    queryset = AutoParkModel.objects.all()
    permission_classes = (IsAuthenticated,)


class AutoParkAddCarView(GenericAPIView):
    queryset = AutoParkModel.objects.all()
    permission_classes = (IsAuthenticated,)

    def post(self, *args, **kwargs):
        data = self.request.data
        serializer = CarSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        auto_park = self.get_object()
        serializer.save(auto_park=auto_park)
        park_serializer = AutoParkSerializer(auto_park)
        return Response(park_serializer.data, status.HTTP_201_CREATED)
