from rest_framework.serializers import ModelSerializer
from .models import Bank, Coin, Rate, Load


class BankSerializer(ModelSerializer):
    class Meta:
        model = Bank
        fields = '__all__'


class CoinSerializer(ModelSerializer):
    class Meta:
        model = Coin
        fields = '__all__'


class RateSerializer(ModelSerializer):
    class Meta:
        model = Rate
        fields = '__all__'


class LoadSerializer(ModelSerializer):
    class Meta:
        model = Load
        fields = '__all__'
