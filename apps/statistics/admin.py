from django.contrib import admin

from apps.statistics.models import RatesPrediction, RatesPredictionText


@admin.register(RatesPrediction)
class RatesPredictionAdmin(admin.ModelAdmin):
    list_display = ('id', 'currency', 'rate_sell', 'date',)
    search_fields = ('id', 'currency', 'rate_sell', 'date',)


@admin.register(RatesPredictionText)
class RatesPredictionTextAdmin(admin.ModelAdmin):
    list_display = ('id', 'currency', 'message',)
    search_fields = ('id', 'currency', 'message',)
