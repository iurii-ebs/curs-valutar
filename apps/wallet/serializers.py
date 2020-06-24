from rest_framework import serializers
from django.db import models
from apps.wallet.models import (Currency,
                                RatesHistory,
                                Wallet,
                                WalletOperations)


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class RatesHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = RatesHistory
        fields = '__all__'


class CurrentRatesSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()

    class Meta:
        model = RatesHistory
        fields = ['rate', 'date', 'currency']


class WalletSerializer(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = '__all__'


class WalletOperationsSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletOperations
        fields = '__all__'
