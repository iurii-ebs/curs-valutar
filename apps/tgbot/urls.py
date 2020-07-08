from django.urls import path
from .views import TelegramRegisterView, TelegramTestNotificationView


urlpatterns = [
    path('register/', TelegramRegisterView.as_view(), name='telegram-register'),
    path('notify/', TelegramTestNotificationView.as_view(), name='telegram-test'),
]
