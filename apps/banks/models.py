from django.db import models
from django.contrib.auth.models import User
from apps.wallet.models import Bank
from apps.wallet.models import RatesHistory as Rate
from apps.wallet.models import Currency as Coin
from apps.commons.models import BaseModel


class Load(BaseModel):
    date = models.DateField(blank=True)
