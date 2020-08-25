from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers

from apps.users.models import AlertPreference


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('first_name', 'last_name', 'email', 'username', 'password')
        extra_kwargs = {
            'email': {'required': True, 'allow_blank': False},
            'password': {'write_only': True},
        }


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True, allow_blank=False)


class PasswordChangeSerializer(serializers.Serializer):
    password1 = serializers.CharField(required=True, allow_blank=False, write_only=True, max_length=50)
    password2 = serializers.CharField(required=True, allow_blank=False, write_only=True, max_length=50)

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise ValidationError("Passwords aren't equal")

        return attrs


class AlertPreferenceSerializer(serializers.ModelSerializer):
    class Meta:
        model = AlertPreference
        fields = '__all__'
