from django.contrib.auth.models import User
from apps.wallet.models import Currency, Bank, RatesHistory
from apps.statistics.models import RatesPrediction, RatesPredictionText
from django.test import Client
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from datetime import date


class PredictionTests(APITestCase):

    def setUp(self):
        self.client = APIClient()
        self.test_user1 = User.objects.create(username='user')
        self.test_user1.set_password('password')
        self.client.force_authenticate(self.test_user1)

        self.bank = Bank.objects.create(
            registered_name='ENERGBANK',
            short_name='energbank'
        )

        self.currency = Currency.objects.create(
            bank=self.bank,
            name='Euro',
            abbr='EUR'
        )

        self.ratesprediction = RatesPrediction.objects.create(
            currency=self.currency,
            rate_sell=19.8,
            date=date.today()
        )

        self.ratehistory = RatesHistory.objects.create(
            currency=self.currency, rate_sell='19.65', rate_buy='19.97', date=date.today()
        )

    def test_get_rates_predicted_list(self):
        response = self.client.get('/statistics/predict/')
        self.assertEqual(response.status_code, 200)

    def test_get_rate_prediction_item(self):
        response = self.client.get('/statistics/predict/1/')
        self.assertEqual(response.status_code, 200)

    def test_get_rate_live_today(self):
        response = self.client.get('/statistics/live/')
        self.assertEqual(response.status_code, 200)

