from rest_framework import serializers

from apps.wallet.models import (
                                Bank,
                                Currency,
                                RatesHistory,
                                Wallet,
                                WalletOperation)


class BankSelectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bank
        fields = ['id', 'short_name', 'registered_name', 'logo_path']


class CurrencySelectionSerializer(serializers.ModelSerializer):
    bank = BankSelectionSerializer(required=False)

    class Meta:
        model = Currency
        fields = ['id', 'abbr', 'bank']


class CurrencySerializer(serializers.ModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class RatesHistorySerializer(serializers.ModelSerializer):
    currency = CurrencySelectionSerializer(required=False)

    class Meta:
        model = RatesHistory
        fields = '__all__'


class CurrentRatesSerializer(serializers.ModelSerializer):
    currency = CurrencySerializer()

    class Meta:
        model = RatesHistory
        fields = ['rate_sell', 'rate_buy', 'date', 'currency']


class WalletSerializerBase(serializers.ModelSerializer):
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
        return float(0.00) if transactions_sum == 0.0 else transactions_sum

    def get_value_buy(self, obj):
        queryset = Wallet.objects.get(user=obj.user, id=obj.id).operationitem.all()
        value_day_bought = sum([(i.rate.rate_buy * i.amount) for i in queryset])
        return float(0.00) if value_day_bought == 0.0 else value_day_bought

    def get_value_sell(self, obj):
        queryset = Wallet.objects.get(user=obj.user, id=obj.id).operationitem.all()
        currency_bought = obj.currency
        rates_currency_bought = RatesHistory.objects.filter(currency=currency_bought).order_by('date')
        currency_rate_today = [i.rate_sell for i in rates_currency_bought][-1:][0]
        value_today = sum([(currency_rate_today * i.amount) for i in queryset])
        return float(0.00) if value_today == 0.0 else value_today

    def get_profit(self, obj):
        value_buy = self.get_value_buy(obj)
        value_sell = self.get_value_sell(obj)
        profit = value_sell - value_buy
        return float(0.00) if profit == 0.0 else profit


class WalletSerializer(WalletSerializerBase):
    currency = CurrencySelectionSerializer(required=False)

    class Meta:
        model = Wallet
        fields = ['id', 'user', 'currency', 'balance', 'value_buy', 'value_sell', 'profit']


class WalletSerializerCreate(WalletSerializerBase):
    class Meta:
        model = Wallet
        fields = ['id', 'user', 'currency', 'balance', 'value_buy', 'value_sell', 'profit']

    def __init__(self, *args, **kwargs):
        super(WalletSerializerCreate, self).__init__(*args, **kwargs)
        self.fields['user'].required = False


class WalletSerializerCreateSWAGGER(serializers.ModelSerializer):
    class Meta:
        model = Wallet
        fields = ['currency']


class WalletOperationCreateSWAGGER(serializers.ModelSerializer):
    class Meta:
        model = WalletOperation
        fields = ['currency', 'amount']


class WalletOperationSerializer(serializers.ModelSerializer):
    currency = CurrencySelectionSerializer(required=False)

    class Meta:
        model = WalletOperation
        fields = '__all__'


class WalletOperationCreateSerializer(serializers.ModelSerializer):
    wallet = WalletSerializer(required=False)

    class Meta:
        model = WalletOperation
        fields = '__all__'
        extra_kwargs = {
            "rate": {"required": False}
        }
