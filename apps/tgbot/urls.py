from django.conf import settings
from django.urls import path
from .views import WebHookView


urlpatterns = [
    path(settings.BOT_TOKEN + '/', WebHookView.as_view(), name='bot-web-hook'),
]
