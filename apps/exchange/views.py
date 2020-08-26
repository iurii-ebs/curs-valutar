from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.exchange.models import Bank, Coin, Rate
from apps.exchange.filtersets import BankFilterSet, CoinFilterSet, RateFilterSet, RatesPredictionFilterSet
from apps.exchange.serializers import BankSerializer, CoinSerializer, RateSerializer
from apps.statistics.models import RatesPrediction
from apps.statistics.serializers import RatesPredictionSerializer

class BankListView(ListAPIView):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = BankFilterSet


class CoinListView(ListAPIView):
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = CoinFilterSet


class RateListView(ListAPIView):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RateFilterSet


class RatesPredictionListView(ListAPIView):
    queryset = RatesPrediction.objects.all()
    serializer_class = RatesPredictionSerializer
    permission_classes = [AllowAny]
    filter_backends = [DjangoFilterBackend]
    filterset_class = RatesPredictionFilterSet
