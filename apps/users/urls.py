from django.urls import re_path
from rest_framework_simplejwt import views as jwt_views

from apps.users import views


re_uid = r'(?P<uid_encoded>[0-9A-Za-z_\-]+)/'
re_token = r'(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/'

urlpatterns = [
    re_path(r'profile/', views.ProfileView.as_view(), name='user_profile'),
    re_path(r'preferences/', views.AlertPreferencesView.as_view(), name='user_preferences'),
    re_path(r'register/', views.RegisterView.as_view(), name='user_register'),
    re_path(r'register-done/', views.RegisterDoneView.as_view(), name='user_register_done'),
    re_path(r'activate/' + re_uid + re_token, views.ActivateView.as_view(), name='user_activate'),
    re_path(r'activate-done/', views.ActivateDoneView.as_view(), name='user_activate_done'),
    re_path(r'token-obtain/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain'),
    re_path(r'token-refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    re_path(r'password-reset/', views.PasswordResetView.as_view(), name='password_reset'),
    re_path(r'password-reset-done/', views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    re_path(r'password-change/' + re_uid + re_token, views.PasswordChangeView.as_view(), name='password_change'),
    re_path(r'password-change-done/', views.PasswordChangeDoneView.as_view(), name='password_change_done'),
]
