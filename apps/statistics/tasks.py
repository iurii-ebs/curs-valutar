import datetime

from celery import shared_task
from notifications.signals import notify
from sklearn.linear_model import LinearRegression

from apps.statistics.models import RatesPrediction, RatesPredictionText
from apps.wallet.models import Currency, RatesHistory
from apps.wallet.models import Wallet
from apps.notification.models import CustomContentType
from apps.users.models import AlertPreference
from apps.commons.tasks import push_notify


@shared_task(name='update_rate_prediction')
def update_rate_prediction(days_to_predict):
    RatesPrediction.objects.all().delete()  # Clear old predicted rates to update based on new actual rate today
    RatesPredictionText.objects.all().delete()
    currency_items = [currency_item.id for currency_item in
                      Currency.objects.all()]  # Make an array of currency IDs currently present in Currency table
    for currency_id in currency_items:  # For each currency ID get its sell history and create an array. Example: [17.2, 17.3, 17.4 ...] and send this data to model_predict_linear() plus how many days to predict
        rates_sequence = [past_rate.rate_sell for past_rate in
                          RatesHistory.objects.filter(currency=currency_id).order_by('date')]
        model_predict_linear(currency_id, rates_sequence, days_to_predict_left=days_to_predict,
                             index_predicted_days=days_to_predict)


def model_predict_linear(currency_id, rates_sequence, days_to_predict_left, index_predicted_days):
    """
    The next 6 lines of code will format array of data in to two 2D arrays compatible with LinearRegression sklearn model
    array X representing all rates that can be yesterday rates
    array Y representing all rates tht can be tomorrow rates
    rates_sequence = [17.05, 17.06, 17.07, 17.08]
    New result:
    yesterday_rates_coord_x = [[17.05], [17.06], [17.07], [17.08]]
    tomorrow_rates_coord_y = [[17.006], [17.07], [17.08], [tomorrow_rate_new_coord_y]]
    """
    if len(rates_sequence) % 2 == 0:
        data = rates_sequence
    else:
        data = rates_sequence[1:]
    yesterday_rates_coord_x = [[i] for i in data[:-1]]
    tomorrow_rates_coord_y = [[i] for i in data[1:]]

    linear_model = LinearRegression()  # Instantiate new model
    linear_model.fit(yesterday_rates_coord_x,
                     tomorrow_rates_coord_y)  # Train model with the formated data from two 2D arrays
    yesterday_rate_new_coord_x = [tomorrow_rates_coord_y[-1]]
    tomorrow_rate_new_coord_y = linear_model.predict(yesterday_rate_new_coord_x)[0][
        0]  # Based on previous data linear model will generate a most likely Y continuation
    rates_sequence += [round(tomorrow_rate_new_coord_y, 4)]  # Append the new predicted sell_rate to initial array rates_sequence
    if days_to_predict_left == 1:  # Entire function predicts +1 day recursively, recursion breaks when there are no more days left to predict
        analyst_agent(currency_id, rates_sequence,
                      index_predicted_days)  # Send currency ID which was predicted and old rates + new rates to analyst_agent()
        create_rate_predictions(currency_id, rates_sequence[
                                             - index_predicted_days:])  # This function will save only the new predicted rates in the RatesPrediction table
        return
    days_to_predict_left -= 1
    model_predict_linear(currency_id, rates_sequence, days_to_predict_left, index_predicted_days)


def create_rate_predictions(currency_id, rates_future):
    """
    Save predicted data into database
    """
    currency = Currency.objects.get(id=currency_id)
    for day, rate_future in enumerate(rates_future):
        RatesPrediction.objects.create(
            currency=currency,
            rate_sell=round(rate_future, 2),
            date=datetime.date.today() + datetime.timedelta(day + 1)
        )


def analyst_agent(currency_id, rates_past_future, days_predicted):
    """
    Analyst agent will calculate expected % and $ growth then forward new + old data to the notification_agent()
    """
    currency = Currency.objects.get(id=currency_id)
    rate_yesterday = rates_past_future[:-days_predicted][-2]
    rate_today = rates_past_future[:-days_predicted][-1]
    rate_end = rates_past_future[-1]
    rate_growth_last_day = rate_today - rate_yesterday
    expected_rate_growth = rate_end - rate_today
    percentage_growth_last_day = 100 * float(rate_growth_last_day) / float(rate_yesterday)
    percentage_growth = 100 * float(expected_rate_growth) / float(rate_today)
    notification_agent(currency, expected_rate_growth, percentage_growth, days_predicted, rate_today, rate_end, percentage_growth_last_day)


def notification_agent(currency, expected_rate_growth, percentage_growth, days_predicted, rate_today, rate_end, percentage_growth_last_day):
    """
    Notification agent will generate a message which will look like:
    'US Dollar from Moldova Agroindbank is expected to rise by 0.32¢ (1.88% UP), for the next 7 days from 17.200 to 17.523'
    """
    notification_verb = f'{currency.name} from {currency.bank} is expected to {"fall" if percentage_growth < 0 else "rise"} by {abs(expected_rate_growth):.2f}¢ ({percentage_growth:.2f}% {"DOWN" if percentage_growth < 0 else "UP"}), for the next {days_predicted} days from {rate_today:.3f} to {rate_end:.3f}'
    wallets = Wallet.objects.all()
    preferences = AlertPreference.objects.all()

    content_type = CustomContentType.objects.get(id=1)
    for wallet in wallets:
        user_alert_preferences = preferences.filter(user=wallet.user).first()
        trigger_forecast = getattr(user_alert_preferences, 'percentage_down_forecast', 0)
        trigger_last_day = getattr(user_alert_preferences, 'percentage_down', 0)
        RatesPredictionText.objects.get_or_create(
            currency=currency,
            message=notification_verb,
        )
        if wallet.currency_id == currency.id:
            notify.send(wallet.user,
                        recipient=wallet.user,
                        action_object=content_type,
                        verb=notification_verb,
                        target=currency)
            if trigger_forecast != 0 and percentage_growth < 0 and abs(percentage_growth) > trigger_forecast:
                push_notify(user=wallet.user, title=f"Price forecast alert", message=f"Warning price for {currency.name} is expected to fall by {round(percentage_growth, 2)}% by the next week.")

            if trigger_last_day != 0 and percentage_growth_last_day < 0 and abs(percentage_growth_last_day) > trigger_last_day:
                push_notify(user=wallet.user, title="Price fall alert", message=f"Warning price for {currency.name} fell by {round(percentage_growth_last_day, 2)}%")
