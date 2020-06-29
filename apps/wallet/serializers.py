from rest_framework import serializers

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
    value_buy = serializers.SerializerMethodField()
    value_sell = serializers.SerializerMethodField()
    profit = serializers.SerializerMethodField()

    class Meta:
        model = Wallet
        fields = ['id', 'user', 'currency', 'balance', 'value_buy', 'value_sell', 'profit']

    def get_balance(self, obj):
        queryset = Wallet.objects.get(user=obj.user, id=obj.id).operationitem.all()
        transactions_sum = sum([i.amount for i in queryset])
        return transactions_sum

    def get_value_buy(self, obj):
        queryset = Wallet.objects.get(user=obj.user, id=obj.id).operationitem.all()
        value_day_bought = sum([(i.rate.rate * i.amount) for i in queryset])
        return value_day_bought

    def get_value_sell(self, obj):
        queryset = Wallet.objects.get(user=obj.user, id=obj.id).operationitem.all()
        currency_bought = obj.currency
        rates_currency_bought = RatesHistory.objects.filter(currency=currency_bought).order_by('date')
        currency_rate_today = [i.rate for i in rates_currency_bought][-1:][0]
        value_today = sum([(currency_rate_today * i.amount) for i in queryset])
        return value_today

    def get_profit(self, obj):
        value_buy = self.get_value_buy(obj)
        value_sell = self.get_value_sell(obj)
        return value_sell - value_buy


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
