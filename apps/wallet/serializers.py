from rest_framework import serializers
from django.db import models
from apps.wallet.models import (Currency,
                                RatesHistory,
                                Wallet,
                                WalletOperation)


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


class WalletOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletOperation
        fields = '__all__'
