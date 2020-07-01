from django.contrib import admin
from django.urls import path, include
from rest_framework.permissions import AllowAny
from drf_yasg import openapi
from drf_yasg.views import get_schema_view

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
    path('parser/', include("apps.currency_parser.urls")),
    path('wallets/', include("apps.wallet.urls")),
    path('statistics/', include("apps.statistics.urls")),
    path('notifications/', include('notifications.urls', namespace='notifications')),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
]
