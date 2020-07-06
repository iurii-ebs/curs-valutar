from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from apps.wallet.models import Bank
from apps.wallet.models import RatesHistory as Rate
from apps.wallet.models import Currency as Coin


class Load(models.Model):
    date = models.DateField(blank=True, input_formats=settings.DATE_INPUT_FORMATS)
