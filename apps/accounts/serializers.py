from rest_framework.serializers import Serializer, CharField
from rest_framework.serializers import *


class FirebaseTokenSerializer(Serializer):
    token = CharField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class FirebaseSignupSerializer(Serializer):
    email = EmailField()
    password = CharField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass


class FirebaseSigninSerializer(Serializer):
    email = EmailField()
    password = CharField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
