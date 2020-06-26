from django.db import models
from django.contrib.auth.models import User


class Bank(models.Model):
    registered_name = models.CharField(max_length=50)
    website = models.CharField(max_length=50, default='')

    def __str__(self):
        return '{}'.format(
            self.registered_name
        )


class Currency(models.Model):
    bank = models.ForeignKey(
        Bank, related_name='rateprovider', default=1, blank=True, on_delete=models.CASCADE
    )
    name = models.CharField(max_length=50)
    abbr = models.CharField(max_length=50)

    def __str__(self):
        return 'Bank: {}, {}'.format(
            self.bank, self.abbr
        )


class RatesHistory(models.Model):
    currency = models.ForeignKey(
        Currency, related_name='currencyitem', on_delete=models.CASCADE
    )
    rate = models.FloatField()
    date = models.DateField(db_index=True, auto_now_add=True)

    def __str__(self):
        return '{}, Rate: {}, {}'.format(
            self.currency, self.rate, self.date
        )


class Wallet(models.Model):
    user = models.ForeignKey(
        User, related_name='walletitem', on_delete=models.CASCADE
    )
    currency = models.ForeignKey(
        Currency, related_name='historyitem', on_delete=models.CASCADE
    )

    def __str__(self):
        return 'User: {}, Currency: {}'.format(
            self.user, self.currency
        )


class WalletOperation(models.Model):
    wallet = models.ForeignKey(
        Wallet, related_name='operationitem', on_delete=models.CASCADE
    )
    rate = models.ForeignKey(
        RatesHistory, related_name='historyitem', on_delete=models.CASCADE
    )
    amount = models.FloatField()

    def __str__(self):
        return '{}, {}, {}'.format(
            self.wallet, self.rate, self.amount
        )
