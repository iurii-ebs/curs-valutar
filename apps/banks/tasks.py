import json
import requests
from celery import shared_task
from django.conf import settings
from rest_framework import status

from .models import Bank, Coin, Rate


@shared_task()
def create_rates(date):
    """ Authorize to BANK PARSER and request rates """
    # Request JWT authentication access token
    token_request = requests.post(
        url=f'http://{settings.BANK_PARSER_HOST}:{settings.BANK_PARSER_PORT}/api/user/token/',
        data={
            'username': settings.BANK_PARSER_USERNAME,
            'password': settings.BANK_PARSER_PASSWORD,
        }
    )

    # Check request status
    if token_request.status_code != status.HTTP_200_OK:
        return json.dumps(obj={
            'ok': False,
            'detail': f'Request token failed with code {token_request.status_code}'
        })

    # Request rates JSON
    rates_request = requests.get(
        url=f'http://{settings.BANK_PARSER_HOST}:{settings.BANK_PARSER_PORT}/banks/get/all/?date={date}',
        headers={
            "Authorization": f'Bearer {token_request.json["access"]}'
        }
    )

    # Check request status
    if rates_request.status_code != status.HTTP_200_OK:
        return json.dumps(obj={
            'ok': False,
            'detail': f"Request rates failed with code {token_request.status_code}"
        })

    # Check if rates request response is JSON
    try:
        rates_json = json.loads(rates_request.text)
    except ValueError:
        return json.dumps(obj={
            'ok': False,
            'detail': f"Can't parse rates request to JSON: {rates_request.text}",
        })

    # TODO: Validate JSON Schema

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
    detail['Coin']['skipped'] = count - detail['Bank']['created']
    detail['Rate']['skipped'] = count - detail['Bank']['created']

    return json.dumps({
        'ok': True,
        'detail': detail,
    })
