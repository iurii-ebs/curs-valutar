import datetime
from django.conf import settings
from apps.wallet.models import Currency, RatesHistory

from apps.statistics.models import RatesPrediction

from celery import shared_task

import matplotlib.pyplot as plt

import os
import subprocess


# @shared_task(name='gen_pdf_graphs')
def gen_pdf_graphs(currency_id):
    workdir = f"{settings.STATIC_ROOT}/graphs/{currency_id}"
    curs_valutar_dir_check = os.path.isdir(workdir)
    if curs_valutar_dir_check:
        pass
    else:
        subprocess.call(["mkdir", "-p", workdir])

    queryset_h = RatesHistory.objects.filter(currency_id=currency_id, date__lte=datetime.datetime.today(),
                                             date__gt=datetime.datetime.today() - datetime.timedelta(days=7))
    queryset_p = RatesPrediction.objects.filter(currency_id=currency_id)

    currency = Currency.objects.get(id=currency_id)

    data_historyX = [f"{rate.date}" for rate in queryset_h]
    data_historyY = [rate.rate_sell for rate in queryset_h]
    data_predictX = [f"{rate.date}" for rate in queryset_p]
    data_predictY = [rate.rate_sell for rate in queryset_p]
    gen_pdf_graph_past(data_historyX, data_historyY, currency, workdir)
    gen_pdf_graph_future(data_predictX, data_predictY, currency, workdir)
    gen_pdf_graph_past_future(data_historyX + data_predictX, data_historyY + data_predictY, currency, workdir)


def gen_pdf_graph_past(x, y, currency, workdir):
    fig, ax = plt.subplots()
    ax.set_xlabel('Date')
    ax.set_ylabel('Rate Sell')
    ax.plot(x, y)
    ax.grid(True)

    fig.autofmt_xdate()
    fig.set_figheight(6)
    fig.set_figwidth(6)
    plt.title(f"{currency.bank} {currency.abbr} - History")
    plt.savefig(f"{workdir}/past.png")


def gen_pdf_graph_future(x, y, currency, workdir):
    fig, ax = plt.subplots()
    ax.set_xlabel('Date')
    ax.set_ylabel('Rate Sell')
    ax.plot(x, y)
    ax.grid(True)

    fig.autofmt_xdate()
    fig.set_figheight(6)
    fig.set_figwidth(6)
    plt.title(f"{currency.bank} {currency.abbr} - Prediction")
    plt.savefig(f"{workdir}/future.png")


def gen_pdf_graph_past_future(x, y, currency, workdir):
    fig, ax = plt.subplots()
    ax.set_xlabel('Date')
    ax.set_ylabel('Rate Sell')
    ax.plot(x, y)
    ax.grid(True)

    fig.autofmt_xdate()
    fig.set_figheight(6)
    fig.set_figwidth(12)
    plt.title(f"{currency.bank} {currency.abbr} - History and Predicted")
    plt.savefig(f"{workdir}/past_future.png")
