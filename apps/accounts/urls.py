from django.urls import path
from apps.accounts import views


urlpatterns = [
    path('firebase-token/', views.FirebaseTokenView.as_view(), name='firebase-token'),
    path('firebase-signup/', views.FirebaseSignupView.as_view(), name='firebase-signup'),
    path('firebase-signin/', views.FirebaseSigninView.as_view(), name='firebase-signin'),
    path('firebase-header/', views.FirebaseHeaderView.as_view(), name='firebase-header'),
]
