from rest_framework import serializers
from django.db.models import Q

from apps.wallet.models import (Currency,
                                RatesHistory,
                                Wallet,
                                WalletOperation)

from apps.users.serializers import UserSerializer


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
    balance = serializers.SerializerMethodField()

    class Meta:
        model = Wallet
        fields = ['id', 'user', 'currency', 'balance']

    def get_balance(self, obj):
        queryset = Wallet.objects.get(Q(user=obj.user) & Q(id=obj.id)).operationitem.all()
        return sum([i.amount for i in queryset])


class WalletSerializerCreate(serializers.ModelSerializer):
    user = UserSerializer(required=False)

    class Meta:
        model = Wallet
        fields = '__all__'


class WalletOperationSerializer(serializers.ModelSerializer):
    class Meta:
        model = WalletOperation
        fields = '__all__'


class WalletOperationSerializerCreate(serializers.ModelSerializer):
    wallet = WalletSerializer(required=False)

    class Meta:
        model = WalletOperation
        fields = '__all__'
