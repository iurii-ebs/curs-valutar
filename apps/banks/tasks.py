import json
import jsonschema
import requests
import datetime
from celery import shared_task
from django.conf import settings
from rest_framework import status
from .models import Bank, Coin, Rate


@shared_task(name="create_rates")
def create_rates(date=datetime.datetime.today()):
    """ Authorize to BANK PARSER and request rates """
    # Request rates JSON
    try:
        rates_request = requests.get(
            url=f'http://{settings.BANK_PARSER_HOST}:{settings.BANK_PARSER_PORT}/banks/get/all/?date={date}',
            timeout=60,
        )
    except Exception as e:
        return {
            'ok': False,
            'detail': f'Rates request failed with exception {e}',
        }

    # Check rates request status
    if rates_request.status_code != status.HTTP_200_OK:
        return {
            'ok': False,
            'detail': f"Rates request failed with status {rates_request.status_code}",
        }

    # Check if rates request response is JSON
    try:
        rates_json = json.loads(rates_request.text)
    except ValueError:
        return {
            'ok': False,
            'detail': f"Rates JSON parsing failed {rates_request.text}",
        }

    # Check if rates_json is a list
    if not isinstance(rates_json, list):
        return {
            'ok': False,
            'detail': f'Rates JSON is not a list',
        }

    # Check if rates_json items have valid schema
    try:
        for item in rates_json:
            jsonschema.validate(instance=item, schema=settings.BANK_PARSER_SCHEMA)
    except jsonschema.exceptions.ValidationError:
        return {
            'ok': False,
            'detail': f"Rates JSON schema validation failed"
        }

    # Create instances
    detail = {
        'Bank': {'created': 0, 'skipped': 0},
        'Coin': {'created': 0, 'skipped': 0},
        'Rate': {'created': 0, 'skipped': 0},
    }

    count = len(rates_json)

    for item in rates_json:
        bank, created = Bank.objects.get_or_create(
            registered_name=item['bank']['name'],
            short_name=item['bank']['short_name'],
        )
        if created:
            detail['Bank']['created'] += 1

        coin, created = Coin.objects.get_or_create(
            name=item['currency']['name'],
            abbr=item['currency']['abbr'],
            bank=bank,
        )
        if created:
            detail['Coin']['created'] += 1

        rate, created = Rate.objects.get_or_create(
            currency=coin,
            rate_sell=item['rate_sell'],
            rate_buy=item['rate_buy'],
            date=item['date'],
        )
        if created:
            detail['Rate']['created'] += 1

    detail['Bank']['skipped'] = count - detail['Bank']['created']
    detail['Coin']['skipped'] = count - detail['Coin']['created']
    detail['Rate']['skipped'] = count - detail['Rate']['created']

    return {
        'ok': True,
        'detail': detail,
    }

