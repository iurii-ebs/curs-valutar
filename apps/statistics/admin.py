from django.contrib import admin
from apps.statistics.models import RatesPrediction, RatesPredictionText

admin.site.register(RatesPrediction)
admin.site.register(RatesPredictionText)
