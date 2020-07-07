from django.db import models
from django.contrib.auth import get_user_model


class TelegramUser(models.Model):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    token = models.CharField(max_length=16)
    chat_id = models.IntegerField(blank=True, null=True)
