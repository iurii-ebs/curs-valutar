from django.db import models

from django.contrib.auth.models import User
from apps.commons.models import BaseModel


class AlertPreference(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    alert_down = models.IntegerField(null=True, blank=True, default=3)
    alert_down_forecast = models.IntegerField(null=True, blank=True, default=3)
