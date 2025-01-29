from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase

from apps.auto_parks.models import AutoParkModel
from apps.cars.models import CarModel

UserModel = get_user_model()

class CarApiTestCase(APITestCase):
    def setUp(self):
        self.auto_park_id = AutoParkModel.objects.create(
            name='Uber'
        ).id

        self.car1 = CarModel.objects.create(
            model="BMW",
            body_type="Jeep",
            price=2000,
            year=2000,
            auto_park_id=self.auto_park_id
        )

        self.car2 = CarModel.objects.create(
            model="AUDI",
            body_type="Sedan",
            price=3000,
            year=2001,
            auto_park_id=self.auto_park_id
        )

    def _authenticate(self):
        user = UserModel.objects.create_user(email='admin@gmail.com', password='P@$$word1', is_active=True)
        res = self.client.post(reverse('auth_login'), {'email': user.email, 'password': 'P@$$word1'})
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + res.data['access'])

    def test_get_all_cars(self):
        res = self.client.get(reverse('cars_create_list'))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        data = res.data
        self.assertEqual(len(data), 2)
        car1 = CarModel.objects.get(pk=self.car1.pk)
        self.assertEqual(car1.model, "BMW")
        car2 = CarModel.objects.get(pk=self.car2.pk)
        self.assertEqual(car2.model, "AUDI")
        self.assertEqual(CarModel.objects.count(), 2)

    def test_create_car_without_auth(self):
        data = {
            'model': 'OKA',
            'body_type': 'Jeep',
            'price': 200,
            'year': 2000,
        }
        count_before = CarModel.objects.count()
        res = self.client.post(reverse('cars_create_list'), data)
        count_after = CarModel.objects.count()
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(count_before, count_after)


    def test_create_car_with_auth(self):
        self._authenticate()
        data = {
            'model': 'OKA',
            'body_type': 'Jeep',
            'price': 200,
            'year': 2000,
        }
        count_before = CarModel.objects.count()
        res = self.client.post(reverse('cars_create_list'), data)
        count_after = CarModel.objects.count()
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertEqual(count_after, count_before+1)
