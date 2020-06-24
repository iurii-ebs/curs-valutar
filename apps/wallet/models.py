from django.db import models
from django.contrib.auth.models import User


class Currency(models.Model):
    name = models.CharField(max_length=50)
    abbr = models.CharField(max_length=50)


class RatesHistory(models.Model):
    currency = models.ForeignKey(
        Currency, related_name='currencyitem', on_delete=models.CASCADE
    )
    rate = models.FloatField()
    date = models.DateField(db_index=True, auto_now_add=True)


class Wallet(models.Model):
    user = models.ForeignKey(
        User, related_name='walletitem', on_delete=models.CASCADE
    )
    currency = models.ForeignKey(
        Currency, related_name='historyitem', on_delete=models.CASCADE
    )
    total_amount = models.FloatField()


class WalletOperations(models.Model):
    wallet_id = models.ForeignKey(
        Wallet, related_name='operationitem', on_delete=models.CASCADE
    )
    rate_id = models.ForeignKey(
        RatesHistory, related_name='historyitem', on_delete=models.CASCADE
    )
    amount = models.FloatField()
