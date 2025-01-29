from unittest import TestCase
from unittest.mock import MagicMock, patch

from apps.cars.services import calc, math


class CalcTestCase(TestCase):
    @patch.object(math, 'cos')
    def test_plus(self, mock_cos:MagicMock):
        mock_cos.return_value = 25
        res = calc(1, 2, '+')

        self.assertEqual(res, 25)
    @patch('apps.cars.services.sqrt')
    def test_multi(self, mock_sqrt:MagicMock):
        mock_sqrt.return_value = 5
        res = calc(1, 2, '*')
        self.assertEqual(res, 7)
    def test_minus(self):
        res = calc(1, 2, '-')
        self.assertEqual(res, -1)
        