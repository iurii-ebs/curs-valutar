from rest_framework import serializers
from apps.statistics.models import RatesPrediction


class RatesPredictionSerializer(serializers.ModelSerializer):
    class Meta:
        model = RatesPrediction
        fields = '__all__'
