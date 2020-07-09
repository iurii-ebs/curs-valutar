from django.db import models
from django.contrib.auth import get_user_model


class TelegramUser(models.Model):
    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)
    token = models.CharField(max_length=16)
    created = models.DateTimeField(auto_now=True)
    chat_id = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return f'Username: {self.user.username} | chat id: {self.chat_id} | Creation datetime: {self.created}'
