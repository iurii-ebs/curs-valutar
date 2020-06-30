from django.shortcuts import render
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response

from apps.wallet.models import Bank as BankModel
from apps.wallet.models import RatesHistory as RateModel

import json
import requests


class LoadRatesView(GenericAPIView):
    # TODO: Add permission only if user is autenticated as admin
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        # Request data from parser
        response = requests.get('http://127.0.0.2:8000/banks/get/all/')

        # Check response status code
        if response.status_code != 200:
            return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)

        # Parse json
        data = json.loads(response.text)

        # Check data length
        if not len(data):
            return Response(status.HTTP_500_INTERNAL_SERVER_ERROR)

        for item in data:
            pass

        return Response(f'{len(data)}')


# TODO: Remove me
"""
{
    "currency": {
        "name": "US Dollar",
        "abbr": "USD"
    },
    "bank": {
        "name": "Moldova Agroindbank",
        "short_name": "MAIB"
    },
    "rate_sell": 17.02,
    "rate_buy": 17.28,
    "date": "2020-06-30"
},
"""
