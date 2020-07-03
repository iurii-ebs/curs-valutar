from celery import task
import json
import requests

from django.conf import settings
from rest_framework import status

from .models import Bank, Coin, Rate


def get_or_create(model, **kwargs):
    """Try to get instance from specified model or create them if it doesn't exist."""
    try:
        obj = model.objects.get(**kwargs)
    except model.DoesNotExist:
        obj = model.objects.create(**kwargs)

    return obj


def load_item(item):
    """Create (if doesn't exist) bank, coin and rate from json entry."""
    try:
        bank = get_or_create(
            Bank,
            registered_name=item['bank']['name'],
            short_name=item['bank']['short_name'],
        )

        coin = get_or_create(
            Coin,
            name=item['currency']['name'],
            abbr=item['currency']['abbr'],
            bank=bank,
        )

        rate = get_or_create(
            Rate,
            currency=coin,
            rate_sell=item['rate_sell'],
            rate_buy=item['rate_buy'],
            date=item['date'],
        )
    except KeyError:
        return False

    return True


@task.task()
def load_rates(date):
    host = settings.BP_HOST
    port = settings.BP_PORT
    username = settings.BP_USER
    password = settings.BP_PASS

    # Request access token
    access = requests.post(
        url=f'http://{host}:{port}/api/user/token/',
        data={
            'username': username,
            'password': password,
        }
    )

    if access.status_code != status.HTTP_200_OK:
        raise ValueError("Request token failed")

    # Request rates json
    rates = requests.get(
        url=f'http://{host}:{port}/banks/get/all/?date={date}',
        headers={'Authorization': f'Bearer {access.json()["access"]}'},
    )

    if rates.status_code != status.HTTP_200_OK:
        raise ValueError("Request rates failed")

    # Create model instances
    for item in json.loads(rates.text):
        if not load_item(item):
            raise ValueError("JSON unpack failed")
