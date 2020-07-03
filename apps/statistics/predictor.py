from sklearn.linear_model import LinearRegression
import datetime

from apps.wallet.models import Currency

from apps.statistics.models import RatesPrediction
from apps.wallet.models import Wallet
from notifications.signals import notify

from celery import shared_task


@shared_task(name='predict_function')
def predict_function(currency_id, rates_sequence, days, future_days=0):
    if len(rates_sequence) % 2 == 0:
        data = rates_sequence
    else:
        data = rates_sequence[1:]
    x = [[i] for i in data[:-1]]
    y = [[i] for i in data[1:]]

    model = LinearRegression()
    model.fit(x, y)
    yesterday = [y[-1]]
    tomorrow = model.predict(yesterday)[0][0]
    rates_sequence += [tomorrow]
    if days == 1:
        analyst_agent(currency_id, rates_sequence, abs(future_days - 1))
        create_rate_predictions(currency_id, rates_sequence[future_days - 1:])
        return
    days_to_predict = days - 1
    future_days = future_days - 1
    predict_function(currency_id, rates_sequence, days_to_predict, future_days)


def create_rate_predictions(currency_id, rates_future):
    currency = Currency.objects.get(id=currency_id)
    for x in range(len(rates_future)):
        RatesPrediction.objects.create(
            currency=currency,
            rate_sell=rates_future[x],
            date=datetime.date.today() + datetime.timedelta(x + 1)
        )


def analyst_agent(currency_id, rates_past_future, days_predicted):
    currency = Currency.objects.get(id=currency_id)
    rate_today = rates_past_future[:-days_predicted][-1]
    rate_end = rates_past_future[-1]
    expected_rate_growth = rate_end - rate_today
    percentage_growth = 100 * float(expected_rate_growth) / float(rate_today)
    notification_agent(currency, expected_rate_growth, percentage_growth, days_predicted, rate_today, rate_end)


def notification_agent(currency, expected_rate_growth, percentage_growth, days_predicted, rate_today, rate_end):
    notification_verb = f'{currency.name} from {currency.bank} is expected to {"fall" if percentage_growth < 0 else "rise"} by {abs(expected_rate_growth):.2f}¢ ({percentage_growth:.2f}% {"DOWN" if percentage_growth < 0 else "UP"}), for the next {days_predicted} days from {rate_today:.3f} to {rate_end:.3f}'
    wallets = Wallet.objects.all()
    for wallet in wallets:
        if wallet.currency.id == currency.id:
            notify.send(wallet.user, recipient=wallet.user, verb=notification_verb)
