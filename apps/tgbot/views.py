from django.conf import settings
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from .models import TelegramUser
from .serializers import TelegramUserSerializer
from .dispacher import process_new_updates, telegram_user
from .tokens import build_token


class WebHookView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        process_new_updates(request)
        return Response()


class TelegramRegisterViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        token = build_token()

        TelegramUser.objects.create(user=user, token=token)

        url = f'https://t.me/{settings.BOT_NAME}/?start={token}'

        return Response({
            'ok': True,
            'detail': 'Follow link',
            'url': url,
        })


class TelegramNotification(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        users = TelegramUser.objects.filter(chat_id__isnull=False)

        for user in users:
            telegram_user(user.chat_id, "Hello notifications")

        return Response({
            'ok': True,
            'detail': 'Notification has been sent'
        })
