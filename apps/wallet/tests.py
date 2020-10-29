from datetime import date

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework.reverse import reverse
from rest_framework.test import APITestCase, APIClient

from apps.wallet.models import (Currency,
                                Bank,
                                RatesHistory,
                                Wallet,
                                WalletOperation)


class WalletTests(APITestCase):
    """ Database tests """

    def setUp(self):
        self.client = APIClient()
        self.test_user1 = User.objects.create(username='user')
        self.test_user1.set_password('password')
        self.client.force_authenticate(self.test_user1)

        # Bank table test data
        self.test_bank1 = Bank.objects.create(
            registered_name='Victoriabank', short_name='VB', website='https://www.victoriabank.md/ro/currency-history'
        )

        self.test_currency1 = Currency.objects.create(
            bank=self.test_bank1,
            name='Australian Dollar',
            abbr='AUD'
        )

        wallet1 = Wallet.objects.create(
            user=self.test_user1,
            currency=self.test_currency1
        )

        # Rates history table test data
        rate_history1 = RatesHistory.objects.create(
            currency=self.test_currency1, rate_sell='11.8621', rate_buy='11.9615', date=date.today()
        )
        rate_history1.save()

        # Wallet operations table test data
        walletoperations1 = WalletOperation.objects.create(
            wallet=wallet1, currency=self.test_currency1, rate=rate_history1, amount=100000
        )
        walletoperations1.save()

        walletoperations2 = WalletOperation.objects.create(
            wallet=wallet1, currency=self.test_currency1, rate=rate_history1, amount=70000
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

    def test_wallet_operations(self):
        wallet_operations = WalletOperation.objects.filter(wallet=1)
        amount = sum([i.amount for i in wallet_operations])
        self.assertEqual(amount, float(170000))

    def setUp(self):
        self.client = APIClient()
        self.test_user1 = User.objects.get(email='testuser1@example.com')
        self.client.force_authenticate(user=self.test_user1)

    """ Views tests """

    # def test_user_

    def test_wallet_list_view(self):
        response = self.client.get(reverse('wallet_list'), )
        self.assertEqual(response.status_code, 200)

    def test_wallet_detail_view(self):
        response = self.client.get(reverse('wallet_detail', args=[1]), )
        self.assertEqual(response.status_code, 200)

    def test_wallet_transactions_view(self):
        response = self.client.get(reverse('wallet_transactions', args=[1]), )
        self.assertEqual(response.status_code, 200)

    def test_predict_list_view(self):
        response = self.client.get(reverse('predict_list'))
        self.assertEqual(response.status_code, 200)

    def test_predict_detail_view(self):
        response = self.client.get(reverse('predict_detail', args=[1]))
        self.assertEqual(response.status_code, 200)

    def test_predict_days_view(self):
        response = self.client.post(reverse('prediction_days', args=[3]))
        self.assertEqual(response.status_code, 200)
