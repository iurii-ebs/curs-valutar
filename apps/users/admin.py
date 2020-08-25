from django.contrib import admin

from apps.users.models import AlertPreference


@admin.register(AlertPreference)
class AlertPreferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'percentage_down', 'percentage_down_forecast', 'days_forecast',)
    search_fields = ('id',)
