from django.db import models

from django.contrib.auth.models import User
from apps.commons.models import BaseModel


class AlertPreference(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    percentage_down = models.FloatField(null=True, blank=True, default=3)
    percentage_down_forecast = models.FloatField(null=True, blank=True, default=3)
    days_forecast = models.FloatField(null=True, blank=True, default=3)
