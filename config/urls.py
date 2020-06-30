from django.contrib import admin
from django.urls import path, include


urlpatterns = [
    path('admin/', admin.site.urls),
    path('users/', include("apps.users.urls")),
    path('banks/', include("apps.banks.urls")),
    path('parser/', include("apps.currency_parser.urls")),
    path('v1/wallets/', include("apps.wallet.urls")),
    path('statistics/', include("apps.statistics.urls")),
    path('notifications/', include('notifications.urls', namespace='notifications')),
]
