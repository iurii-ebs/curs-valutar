from django.test import TestCase
from django.contrib.auth.models import User
from datetime import date as datecreated

from apps.wallet.models import (Currency,
                                RatesHistory,
                                Wallet,
                                WalletOperations)


class WalletTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        # User table test data
        testuser1 = User.objects.create_user(
            username='testuser1', password='password123'
        )
        testuser1.save()

        # Currency table test data
        testcurrency1 = Currency.objects.create(
            name='Australian Dollar', abbr='AUD'
        )
        testcurrency1.save()

        # Wallet table test data
        wallet1 = Wallet.objects.create(
            user_id=testuser1, currency_id=testcurrency1, total_amount=170000
        )
        wallet1.save()

        # Rates history table test data
        ratehistory1 = RatesHistory.objects.create(
            currency_id=testcurrency1, rate='11.8621'
        )
        ratehistory1.save()

        # Wallet operations table test data
        walletoperations1 = WalletOperations.objects.create(
            wallet_id=wallet1, rate_id=ratehistory1, amount=100000
        )
        walletoperations1.save()

        walletoperations2 = WalletOperations.objects.create(
            wallet_id=wallet1, rate_id=ratehistory1, amount=70000
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
        user_id = f'{wallet.user_id}'
        currency_id = f'{wallet.currency_id}'
        total_amount = wallet.total_amount
        self.assertEqual(user_id, 'testuser1')
        self.assertEqual(currency_id, f'{Currency.objects.get(id=1)}')
        self.assertEqual(total_amount, float(170000))

    def test_rates_history(self):
        rate_history = RatesHistory.objects.get(id=1)
        currency_id = f'{rate_history.currency_id}'
        rate = f'{rate_history.rate}'
        date = f'{rate_history.date}'
        self.assertEqual(currency_id, f'{Currency.objects.get(id=1)}')
        self.assertEqual(rate, '11.8621')
        self.assertEqual(date, f'{datecreated.today()}')

    def test_wallet_operations(self):
        wallet_operations = WalletOperations.objects.filter(wallet_id=1)
        amount = sum([i.amount for i in wallet_operations])
        self.assertEqual(amount, float(170000))
