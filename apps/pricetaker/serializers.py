from rest_framework import serializers

from apps.pricetaker.models import Pricetaker


class PricetakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricetaker
        fields = '__all__'
