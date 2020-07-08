from django.conf import settings
from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from apps.tgbot.views import TelegramWebHookView


schema_view = get_schema_view(
    openapi.Info(
        title="Curs Valutar API Documentation",
        default_version='v1',
        description="Curs  valutar API documentation",
    ),
    validators=['ssv'],
    public=True,
    permission_classes=(AllowAny,)
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include("apps.users.urls")),
    path('banks/', include("apps.banks.urls")),
    path('tgbot/', include("apps.tgbot.urls")),
    path('wallets/', include("apps.wallet.urls")),
    path('statistics/', include("apps.statistics.urls")),
    path('notifications/', include('notifications.urls', namespace='notifications')),
    path(settings.BOT_PATH, TelegramWebHookView.as_view(), name='telegram-webhook'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
