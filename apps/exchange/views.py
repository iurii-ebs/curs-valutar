from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import ListAPIView
from rest_framework.permissions import AllowAny

from apps.exchange.models import Bank, Coin, Rate
from apps.exchange.filtersets import BankFilterSet, CoinFilterSet, RateFilterSet
from apps.exchange.serializers import BankSerializer, CoinSerializer, RateSerializer


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
