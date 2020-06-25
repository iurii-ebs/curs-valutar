from django.urls import path

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

from apps.users.views import RegisterUserView, register_user_view, activate_user_view


activate_pattern = r'activate/(?P<uid_encoded>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/'


urlpatterns = [
    path('register/', register_user_view, name='token_register'),
    path(activate_pattern, activate_user_view, name='activate_user'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
