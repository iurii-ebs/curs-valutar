from django.contrib import admin

from apps.pricesource.models import Pricesource


@admin.register(Pricesource)
class PricesourceAdmin(admin.ModelAdmin):
    list_display = ('id', 'registered_name', 'short_name', 'data_source',)
    search_fields = ('id', 'registered_name', 'short_name', 'data_source',)
