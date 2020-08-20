from django.contrib import admin
from apps.notification.models import CustomContentType


@admin.register(CustomContentType)
class CustomContentTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type', 'description',)
    search_fields = ('id', 'type', 'description',)
