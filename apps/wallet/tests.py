from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date as datecreated
from rest_framework.test import APIClient
from rest_framework.reverse import reverse
from celery.contrib.testing.worker import start_worker
from django.test.utils import override_settings
from config.celery import app
from apps.statistics.predictor import predict_function

from apps.wallet.models import (Currency,
                                Bank,
                                RatesHistory,
                                Wallet,
                                WalletOperation)


class WalletTests(TestCase):
    """ Database tests """

    @classmethod
    def setUpTestData(cls):
        # User table test data
        testuser1 = User.objects.create_user(
            username='testuser1', email='testuser1@example.com', password='password123'
        )
        testuser1.save()

        # Bank table test data
        testbank1 = Bank.objects.create(
            registered_name='Victoriabank', short_name='VB', website='https://www.victoriabank.md/ro/currency-history'
        )
        testbank1.save()

        # Currency table test data
        testcurrency1 = Currency.objects.create(
            bank=testbank1, name='Australian Dollar', abbr='AUD'
        )
        testcurrency1.save()

        # Wallet table test data
        wallet1 = Wallet.objects.create(
            user=testuser1, currency=testcurrency1
        )
        wallet1.save()

        # Rates history table test data
        ratehistory1 = RatesHistory.objects.create(
            currency=testcurrency1, rate_sell='11.8621', rate_buy='11.9615'
        )
        ratehistory1.save()
        ratehistory2 = RatesHistory.objects.create(
            currency=testcurrency1, rate_sell='11.9621', rate_buy='12.0000'
        )
        ratehistory2.save()

        # Wallet operations table test data
        walletoperations1 = WalletOperation.objects.create(
            wallet=wallet1, currency=testcurrency1, rate=ratehistory1, amount=100000
        )
        walletoperations1.save()

        walletoperations2 = WalletOperation.objects.create(
            wallet=wallet1, currency=testcurrency1, rate=ratehistory1, amount=70000
        )
        walletoperations2.save()

    def test_currency(self):
        currency = Currency.objects.get(id=1)
        abbr = f'{currency.abbr}'
        currency_name = f'{currency.name}'
        self.assertEqual(abbr, 'AUD')
        self.assertEqual(currency_name, 'Australian Dollar')

    def test_wallet(self):
        wallet = Wallet.objects.get(id=1)
        user = f'{wallet.user}'
        currency = f'{wallet.currency}'
        self.assertEqual(user, 'testuser1')
        self.assertEqual(currency, f'{Currency.objects.get(id=1)}')

    def test_rates_history(self):
        rate_history = RatesHistory.objects.get(id=1)
        currency = f'{rate_history.currency}'
        rate_sell = f'{rate_history.rate_sell}'
        date = f'{rate_history.date}'
        self.assertEqual(currency, f'{Currency.objects.get(id=1)}')
        self.assertEqual(rate_sell, '11.8621')
        self.assertEqual(date, f'{datecreated.today()}')

    def test_wallet_operations(self):
        wallet_operations = WalletOperation.objects.filter(wallet=1)
        amount = sum([i.amount for i in wallet_operations])
        self.assertEqual(amount, float(170000))

    def setUp(self):
        self.client = APIClient()
        self.test_user1 = User.objects.get(email='testuser1@example.com')

    """ Views tests """

    def test_wallet_list_view(self):
        self.client.force_authenticate(user=self.test_user1)
        response = self.client.get(reverse('wallet_list'), )
        self.assertEqual(response.status_code, 200)

    def test_wallet_detail_view(self):
        self.client.force_authenticate(user=self.test_user1)
        response = self.client.get(reverse('wallet_detail', args=[1]), )
        self.assertEqual(response.status_code, 200)

    def test_wallet_transactions_view(self):
        self.client.force_authenticate(user=self.test_user1)
        response = self.client.get(reverse('wallet_transactions', args=[1]), )
        self.assertEqual(response.status_code, 200)

    def test_predict_list_view(self):
        response = self.client.get(reverse('predict_list'))
        self.assertEqual(response.status_code, 200)

    def test_predict_detail_view(self):
        response = self.client.get(reverse('predict_detail', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_predict_days_view(self):
        self.client.force_authenticate(user=self.test_user1)
        response = self.client.post(reverse('prediction_days', args=[3]))
        self.assertEqual(response.status_code, 200)
