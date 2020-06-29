from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    email = serializers.EmailField()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "username", "password",)


class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField()


class PasswordChangeSerializer(serializers.Serializer):
    password1 = serializers.CharField(required=True, write_only=True, min_length=8, max_length=50)
    password2 = serializers.CharField(required=True, write_only=True, min_length=8, max_length=50)

    def validate(self, attrs):
        if attrs['password1'] != attrs['password2']:
            raise ValidationError("Passwords aren't equal")

        return attrs
