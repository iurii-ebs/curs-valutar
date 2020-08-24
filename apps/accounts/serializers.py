from rest_framework.serializers import Serializer, CharField


class FirebaseTokenSerializer(Serializer):
    token = CharField()

    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass
