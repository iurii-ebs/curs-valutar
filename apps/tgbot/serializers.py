from rest_framework.serializers import ModelSerializer
from .models import TelegramUser


class TelegramUserSerializer(ModelSerializer):
    class Meta:
        model = TelegramUser
        fields = '__all__'
