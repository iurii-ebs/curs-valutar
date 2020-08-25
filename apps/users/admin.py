from django.contrib import admin

from apps.users.models import AlertPreference


@admin.register(AlertPreference)
class AlertPreferenceAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'alert_down', 'alert_down_forecast',)
    search_fields = ('id', 'user__username', 'alert_down', 'alert_down_forecast',)
