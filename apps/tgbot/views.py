from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .dispacher import bot
import telebot


class WebHookView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        update = telebot.types.Update.de_json(request.data)
        bot.process_new_updates([update])

        return Response()
