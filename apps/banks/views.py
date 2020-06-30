from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.response import Response

from apps.wallet.models import (
    Bank as BankModel,
    RatesHistory as RateModel,
    Currency as CoinModel,
)

from apps.wallet.serializers import RatesHistorySerializer

import json
import requests


def get_or_create(model, **kwargs):
    # Return instance from model or create it if doesn't exist
    try:
        obj = model.objects.get(**kwargs)
    except model.DoesNotExist:
        obj = model(**kwargs)
        obj.save()

    return obj


def create_instances(item):
    # Get or create Bank instance
    bank_kwargs = {
        'registered_name': item['bank']['name'],
        'short_name': item['bank']['short_name'],
    }
    bank = get_or_create(BankModel, **bank_kwargs)

    # Get or create Currency instance
    coin_kwargs = {
        'name': item['currency']['name'],
        'abbr': item['currency']['abbr'],
        'bank': bank,
    }
    coin = get_or_create(CoinModel, **coin_kwargs)

    # Get or create RatesHistory instance
    rate_kwargs = {
        'currency': coin,
        'rate_sell': item['rate_sell'],
        'rate_buy': item['rate_buy'],
        'date': item['date'],
    }
    rate = get_or_create(RateModel, **rate_kwargs)

    return rate


class LoadRatesView(GenericAPIView):
    serializer_class = RatesHistorySerializer

    # TODO: Add permission only if user is autenticated as admin
    permission_classes = [AllowAny]
    # Permission_classes = [IsAdminUser]

    @staticmethod
    def get(request):
        # Request data from parser
        response = requests.get('http://127.0.0.2:8000/banks/get/all/')

        # Check response status code
        if response.status_code != 200:
            return Response()

        # For each entry in data create models
        try:
            for item in json.loads(response.text):
                create_instances(item)
        except (KeyError,):
            return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response(status.HTTP_200_OK)
