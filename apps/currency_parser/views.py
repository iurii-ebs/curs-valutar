from django.core.exceptions import ObjectDoesNotExist

from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .parser import parse_currency as parser
from ..wallet.models import Currency, RatesHistory
from .parser import today
from ..wallet.serializers import CurrencySerializer, CurrentRatesSerializer


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
    if not RatesHistory.objects.filter(date=valid_date).exists():
        currency_list = parser()
        for currency in currency_list['Currency_list']:
            # Get object from Currency table to refer in RatesHistory
            currency = Currency.objects.get(abbr=currency['Abbr'])
            rate = RatesHistory()
            rate.currency = currency
            rate.rate = currency['Rate']
            rate.save()

    rates = RatesHistory.objects.filter(date=valid_date)

    serializer = CurrentRatesSerializer(rates, many=True)

    return Response(serializer.data)
