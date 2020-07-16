from rest_framework import serializers
from apps.statistics.models import RatesPrediction, RatesPredictionText


class RatesPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatesPrediction
        fields = '__all__'


class RatesPredictionTextSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatesPredictionText
        fields = '__all__'
