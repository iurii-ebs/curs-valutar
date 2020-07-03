from django.conf import settings
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from .models import Bank, Coin, Rate, Load
from .serializers import BankSerializer, CoinSerializer, RateSerializer, LoadSerializer
from .permissions import IsStaffOrReadOnly

import json
import requests
from datetime import datetime, timedelta


def get_or_create(model, **kwargs):
    """Try to get instance from specified model or create them if it doesn't exist."""
    try:
        obj = model.objects.get(**kwargs)
    except model.DoesNotExist:
        obj = model.objects.create(**kwargs)

    return obj


def load_item(item):
    """Create (if doesn't exist) bank, coin and rate from json entry."""
    try:
        bank = get_or_create(
            Bank,
            registered_name=item['bank']['name'],
            short_name=item['bank']['short_name'],
        )

        coin = get_or_create(
            Coin,
            name=item['currency']['name'],
            abbr=item['currency']['abbr'],
            bank=bank,
        )

        rate = get_or_create(
            Rate,
            currency=coin,
            rate_sell=item['rate_sell'],
            rate_buy=item['rate_buy'],
            date=item['date'],
        )
    except KeyError:
        return False

    return True


def load_item_list(url):
    """Request rates as json and add instances to db"""
    response = requests.get(url)

    if response.status_code != status.HTTP_200_OK:
        return Response("Parser request error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    for item in json.loads(response.text):
        if not load_item(item):
            return Response("JSON keys error", status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    return Response(status.HTTP_200_OK)


class LoadViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Load.objects.all()
    serializer_class = LoadSerializer
    permission_classes = [IsAdminUser]

    def create(self, request):
        # TODO: Когда Макс доделает парсер, добавить в URL дату
        serializer = self.get_serializer()

        date = serializer['date']

        url = settings.BANKS_PARSER['BANKS_ALL'].format(
            host=settings.BANKS_PARSER['HOST']
        )
        return load_item_list(url)


class BankViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    permission_classes = [IsStaffOrReadOnly]

    @action(detail=True)
    def list_coins(self, request, pk):
        coins = Coin.objects.filter(bank=self.get_object())
        return Response(CoinSerializer(coins, many=True).data)


class CoinViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer
    permission_classes = [IsStaffOrReadOnly]

    @action(detail=True)
    def list_rates(self, request, pk):
        rates = Rate.objects.filter(currency=self.get_object())
        return Response(RateSerializer(rates, many=True).data)

    @action(detail=True)
    def list_rates_from(self, request, pk, days=7):
        date_to = datetime.today()
        date_from = date_to - timedelta(days=days)
        rates = Rate.objects.filter(
            currency=self.get_object(),
            date__range=[date_from, date_to]
        )
        return Response(RateSerializer(rates, many=True).data)


class RateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    permission_classes = [IsStaffOrReadOnly]
