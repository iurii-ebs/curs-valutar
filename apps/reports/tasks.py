import datetime
from django.conf import settings
from apps.wallet.models import Currency, RatesHistory

from apps.statistics.models import RatesPrediction
import wget
from celery import shared_task

from weasyprint import HTML
import matplotlib.pyplot as plt
import matplotlib.lines as mlines
import numpy as np


@shared_task(name='gen_static_graphs_all')
def gen_static_graphs_all():
    currencies = Currency.objects.all()
    for index, currency in enumerate(currencies):
        gen_single_graphs(currency.id, currency)


def gen_single_graphs(currency_id, currency):
    workdir = str(settings.STATIC_ROOT) + "/graphs"
    queryset_h = RatesHistory.objects.filter(currency_id=currency_id, date__lte=datetime.datetime.today(),
                                             date__gt=datetime.datetime.today() - datetime.timedelta(days=7))
    queryset_p = RatesPrediction.objects.filter(currency_id=currency_id)

    data_historyX = [f"{rate.date}" for rate in queryset_h]
    data_historyY = [rate.rate_sell for rate in queryset_h]
    data_predictX = [f"{rate.date}" for rate in queryset_p]
    data_predictY = [rate.rate_sell for rate in queryset_p]
    price_today = data_historyY[-1] if len(data_historyY) > 0 else 0
    max_Y = max(data_historyY + data_predictY) + (max(data_historyY + data_predictY) / 200)
    min_Y = min(data_historyY + data_predictY) - (min(data_historyY + data_predictY) / 200)
    gen_pdf_graph_past(data_historyX, data_historyY, min_Y, max_Y, currency, workdir)
    gen_pdf_graph_future(data_predictX, data_predictY, min_Y, max_Y, currency, workdir)
    gen_pdf_graph_past_future(data_historyX + data_predictX, data_historyY + data_predictY, min_Y, max_Y, currency,
                              workdir, price_today, len(data_historyY) - 1)


def gen_pdf_graph_past(x, y, min_Y, max_Y, currency, workdir):
    fig, ax = plt.subplots()

    green_line = mlines.Line2D([], [], color='green', marker='_', linestyle='None',
                               markersize=10, label='price history')

    ax.set_xlabel('Date')
    ax.set_ylabel('Rate Sell')
    ax.plot(x, y, 'green')
    ax.legend(handles=[green_line])

    ax.grid(True)

    fig.autofmt_xdate()
    fig.set_figheight(6)
    fig.set_figwidth(6)
    plt.ylim(min_Y, max_Y)
    plt.title(f"{currency.bank} {currency.abbr} - History")
    plt.savefig(f"{workdir}/{currency.id}_past.png")


def gen_pdf_graph_future(x, y, min_Y, max_Y, currency, workdir):
    fig, ax = plt.subplots()

    red_line = mlines.Line2D([], [], color='red', marker='_', linestyle='None',
                             markersize=10, label='expected price')

    ax.set_xlabel('Date')
    ax.set_ylabel('Rate Sell')
    ax.plot(x, y, 'red')
    ax.legend(handles=[red_line])

    ax.grid(True)

    fig.autofmt_xdate()
    fig.set_figheight(6)
    fig.set_figwidth(6)
    plt.ylim(min_Y, max_Y)
    plt.title(f"{currency.bank} {currency.abbr} - Prediction")
    plt.savefig(f"{workdir}/{currency.id}_future.png")


def gen_pdf_graph_past_future(x, y, min_Y, max_Y, currency, workdir, price_today, today_index):
    fig, ax = plt.subplots()
    ax.set_xlabel('Date')
    ax.set_ylabel('Rate Sell')
    ax.grid(True)

    ax.axhline(price_today, color="black")
    y2 = [price_today for _ in x]
    upper_lim = np.minimum(y2, y)

    red_area = mlines.Line2D([], [], color='crimson', marker='s', linestyle='None',
                             markersize=10, label='(area) lower than today', alpha=0.5)
    green_area = mlines.Line2D([], [], color='limegreen', marker='s', linestyle='None',
                               markersize=10, label='(area) higher than today', alpha=0.5)
    green_line = mlines.Line2D([], [], color='green', marker='_', linestyle='None',
                               markersize=10, label='price history')
    red_line = mlines.Line2D([], [], color='red', marker='_', linestyle='None',
                             markersize=10, label='expected price')
    cyan_circle = mlines.Line2D([], [], color='black', marker='o', linestyle='None',
                                markersize=10, label='today price')

    ax.plot(x, y, color='green')
    ax.plot(x, y2, color='black')
    ax.plot(x[today_index:], y[today_index:], color='red', label='*bar - expected price')
    ax.plot([x[today_index]], [y[today_index]], color='black', marker='o')
    ax.legend(handles=[cyan_circle, green_line, red_line, red_area, green_area])

    ax.fill_between(x, upper_lim, y, facecolor="limegreen", interpolate=True, alpha=0.5)
    ax.fill_between(x, y2, upper_lim, facecolor="crimson", interpolate=True, alpha=0.5)

    fig.autofmt_xdate()
    fig.set_figheight(6)
    fig.set_figwidth(12)
    plt.ylim(min_Y, max_Y)
    plt.title(f"{currency.bank} {currency.abbr} - History and Predicted")
    plt.savefig(f"{workdir}/{currency.id}_past_future.png")


def save_pdf_report_files(pk, filepath, filename):
    file_url = f'http://127.0.0.1:8015/reports/pdf/{pk}'
    dest_file = filepath + filename
    wget.download(file_url, dest_file)
