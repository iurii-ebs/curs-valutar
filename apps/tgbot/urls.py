from django.conf import settings
from django.urls import path
from .views import WebHookView, TelegramRegisterViewSet, TelegramNotification


urlpatterns = [
    path(settings.BOT_TOKEN + '/', WebHookView.as_view(), name='bot-web-hook'),
    path('register/', TelegramRegisterViewSet.as_view(), name='telegram-register'),
    path('notification/', TelegramNotification.as_view(), name='telegram-notification'),
]
