from rest_framework import serializers

from apps.pricesource.models import Pricesource


class PricesourceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pricesource
        fields = '__all__'
