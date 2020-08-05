from celery import shared_task
from apps.pricetaker.models import Pricetaker
from apps.wallet.models import Bank, Currency, RatesHistory
from django.conf import settings
import pandas as pd
import datetime

data_workdir = str(settings.STATIC_ROOT) + "csv"


@shared_task(name='pricetaker_on')
def pricetaker_on(date=str(datetime.datetime.today().date())):
    print(date)  # temporary debug
    get_currency_csv(datetime.datetime.strptime(str(date), '%Y-%m-%d').date())


def get_currency_csv(date):
    pricetakers = Pricetaker.objects.all()
    for index, source in enumerate(pricetakers):
        source_get = f"{source.data_source}&date_end={str(date.strftime('%d.%m.%Y'))}&date_start={str(date.strftime('%d.%m.%Y'))}&bank={source.short_name}"
        data = pd.read_csv(source_get, sep=";")
        data.drop(columns=['Date'], inplace=True)
        currency_to_db(bank=source, data=data, date=date)


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

        if 'buy' in col:
            RatesHistory.objects.filter(currency=currency, rate_sell=0, date=date).update(rate_sell=price)
        if 'sell' in col:
            RatesHistory.objects.filter(currency=currency, rate_buy=0, date=date).update(rate_buy=price)
