from django.db import models
from django.contrib.auth.models import User


class Currency(models.Model):
    name = models.CharField(max_length=50)
    abbr = models.CharField(max_length=50)

    def __str__(self):
        return '{}'.format(
            self.abbr
        )


class RatesHistory(models.Model):
    currency_id = models.ForeignKey(
        Currency, related_name='currencyitem', on_delete=models.CASCADE
    )
    rate = models.FloatField()
    date = models.DateField(db_index=True, auto_now_add=True)

    def __str__(self):
        return '{}, Rate: {}, {}'.format(
            self.currency_id, self.rate, self.date
        )


class Wallet(models.Model):
    user_id = models.ForeignKey(
        User, related_name='walletitem', on_delete=models.CASCADE
    )
    currency_id = models.ForeignKey(
        Currency, related_name='historyitem', on_delete=models.CASCADE
    )
    total_amount = models.FloatField()

    def __str__(self):
        return 'User: {}'.format(
            self.user_id
        )


class WalletOperation(models.Model):
    wallet_id = models.ForeignKey(
        Wallet, related_name='operationitem', on_delete=models.CASCADE
    )
    rate_id = models.ForeignKey(
        RatesHistory, related_name='historyitem', on_delete=models.CASCADE
    )
    amount = models.FloatField()

    def __str__(self):
        return '{}, {}, {}'.format(
            self.wallet_id, self.rate_id, self.amount
        )
