from django.urls import path
from apps.accounts import views


urlpatterns = [
    path('firebase-token/', views.FirebaseTokenView.as_view(), name='firebase-token'),
]
