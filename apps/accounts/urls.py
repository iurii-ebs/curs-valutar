from django.urls import path
from apps.accounts.views import FirebaseTokenView


urlpatterns = [
    path('firebase/', FirebaseTokenView.as_view(), name='firebase'),
]
