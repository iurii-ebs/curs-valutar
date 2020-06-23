from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from .parser import parse_currency as parser
from ..wallet.models import Currency, RatesHistory


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
    return HttpResponse('Currency names was saved')


def parse_currency(request):
    """Parse data in RatesHistory Table"""
    # Should check if date already exists then override (remove all records for selected date)
    currency_list = parser()
    date_raw = currency_list['Date'].split('.')
    valid_date = date_raw[2] + "-" + date_raw[1] + "-" + date_raw[0]
    RatesHistory.objects.filter(date=valid_date).delete()

    for currency in currency_list['Currency_list']:
        # Get object from Currency table to refer in RatesHistory
        currency_id = Currency.objects.get(abbr=currency['Abbr'])
        rate = RatesHistory()
        rate.currency_id = currency_id
        rate.rate = currency['Rate']
        rate.save()
    return HttpResponse(f"Currency for {currency_list['Date']} was saved")
