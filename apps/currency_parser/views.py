from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.core.serializers import serialize
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .parser import parse_currency as parser
from ..wallet.models import Currency, RatesHistory
from .parser import today
from ..wallet.serializers import CurrencySerializer, RatesHistorySerializer


@api_view(['GET'])
@permission_classes([AllowAny])
def parse_currency_first(request):
    """First init of Currency DB"""

    first_currency_list = parser()['Currency_list']
    for currency in first_currency_list:
        curr = Currency()
        try:
            Currency.objects.get(abbr=currency['Abbr'])
            pass
        except ObjectDoesNotExist:
            curr.abbr = currency['Abbr']
            curr.name = currency['Name']
            curr.save()
    currency = Currency.objects.all()
    serializer = CurrencySerializer(currency, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes([AllowAny])
def parse_currency(request):
    """Parse data in RatesHistory Table"""

    # Should check if date already exists then override (remove all records for selected date)
    date_raw = today.split('.')
    valid_date = date_raw[2] + "-" + date_raw[1] + "-" + date_raw[0]

    # if exists data for today get data from DB
    rates = RatesHistory.objects.filter(date=valid_date)
    if len(rates) == 0:
        currency_list = parser()
        for currency in currency_list['Currency_list']:
            # Get object from Currency table to refer in RatesHistory
            currency_id = Currency.objects.get(abbr=currency['Abbr'])
            rate = RatesHistory()
            rate.currency_id = currency_id
            rate.rate = currency['Rate']
            rate.save()
        rates = RatesHistory.objects.filter(date=valid_date)

    serializer = RatesHistorySerializer(rates, many=True)

    return Response(serializer.data)
