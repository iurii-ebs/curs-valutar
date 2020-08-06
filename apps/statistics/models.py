from django.db import models

from apps.wallet.models import Currency
from apps.commons.models import BaseModel


class RatesPrediction(BaseModel):
    currency = models.ForeignKey(
        Currency, related_name='currencypredictions', on_delete=models.CASCADE
    )
    rate_sell = models.FloatField()
    date = models.DateField()

    def es_doc(self):
        return {
            "id": self.id,
            "currency": self.currency_id,
            "rate_sell": self.rate_sell,
            "date": self.date
        }

    def __str__(self):
        return f'ID {self.id}, Currency {self.currency}, Rate sell: {self.rate_sell}, {self.date}'


class RatesPredictionText(BaseModel):
    currency = models.ForeignKey(
        Currency, on_delete=models.CASCADE
    )
    message = models.TextField()

    def __str__(self):
        return f'{self.currency_id} {self.currency} {self.message}'
