from celery import shared_task
from apps.pricesource.models import Pricesource
from apps.wallet.models import Bank, Currency, RatesHistory
from django.conf import settings
import pandas as pd
import datetime
import requests


@shared_task(name='pricesource_trigger')
def pricesource_trigger():
    data = {"date": f"{datetime.datetime.today().date()}"}
    requests.post(settings.HOST_URL + "banks/load/", json=data)


@shared_task(name='pricesource_on')
def pricesource_on(date):
    get_currency_csv(datetime.datetime.strptime(str(date), '%Y-%m-%d').date())


def get_currency_csv(date):
    pricesources = Pricesource.objects.all()
    for index, source in enumerate(pricesources):
        source_get = f"{source.data_source}&date_end={str(date.strftime('%d.%m.%Y'))}&date_start={str(date.strftime('%d.%m.%Y'))}&bank={source.short_name}"
        data = pd.read_csv(source_get, sep=";", decimal=',')
        data.drop(columns=['Data'], inplace=True)
        if len(data.columns.tolist()) > 0:
            currency_to_db(bank=source, data=data, date=date)
        else:
            print('Bank', source.short_name, 'is not yet updated, try later!')


def currency_to_db(bank, data, date):
    columns = data.columns.tolist()
    rows = data.values.tolist()
    n_currency_bank = zip(columns, rows[0])
    for col, price in n_currency_bank:
        bank_obj, created = Bank.objects.get_or_create(
            registered_name=bank.registered_name,
            short_name=bank.short_name,
        )
        currency, created = Currency.objects.get_or_create(
            name=col[:col.index("(")-1],
            abbr=col[col.index("(")+1:col.index("(")+4],
            bank=bank_obj,
        )

        try:
            RatesHistory.objects.get(currency=currency, date=date)
        except:
            RatesHistory.objects.create(
                currency=currency,
                rate_sell=0,
                rate_buy=0,
                date=date,
            )

        if 'cump' in col:
            RatesHistory.objects.filter(currency=currency, rate_sell=0, date=date).update(rate_sell=price)
        if 'vanz' in col:
            RatesHistory.objects.filter(currency=currency, rate_buy=0, date=date).update(rate_buy=price)
