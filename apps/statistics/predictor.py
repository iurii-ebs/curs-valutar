from sklearn.linear_model import LinearRegression
from datetime import date as datecreated

from apps.wallet.models import Currency

from apps.statistics.models import RatesPrediction


def predict_function(currency_id, array, days, future_days=0):
    if len(array) % 2 == 0:
        data = array
    else:
        data = array[1:]
    x = [[i] for i in data[:-1]]
    y = [[i] for i in data[1:]]

    model = LinearRegression()
    model.fit(x, y)
    yesterday = [y[-1]]
    tomorrow = model.predict(yesterday)[0][0]
    array += [tomorrow]
    if days == 1:
        return create_rate_predictions(currency_id, array[future_days - 1:])
    days_to_predict = days - 1
    future_days = future_days - 1
    predict_function(currency_id, array, days_to_predict, future_days)


def create_rate_predictions(currency_id, array):
    date_today = datecreated.today()
    currency = Currency.objects.get(id=currency_id)
    for x in range(len(array)):
        new_prediction_piece = RatesPrediction.objects.create(
            currency=currency,
            rate=array[x],
            date=date_today.replace(date_today.year, date_today.month, date_today.day + x + 1)
        )
        new_prediction_piece.save()
