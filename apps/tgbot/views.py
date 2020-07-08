from datetime import datetime

from django.conf import settings
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import TelegramUser
from .bot import bot_update, bot_notify
from .tokens import build_token


class TelegramWebHookView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        bot_update(request)
        return Response()


class TelegramRegisterView(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        user = request.user

        chat_user = TelegramUser.objects.get_or_create(user=user)
        chat_user.token = build_token()
        chat_user.created = datetime.now()
        chat_user.save()

        url = f'https://t.me/{settings.BOT_NAME}/?start={chat_user.token}'

        return Response({
            'ok': True,
            'detail': 'Follow link',
            'url': url,
        })


class TelegramTestNotificationView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        users = TelegramUser.objects.filter(chat_id__isnull=False)

        for user in users:
            bot_notify(user, "Test notification")

        return Response({
            'ok': True,
            'detail': 'Notification has been sent'
        })
