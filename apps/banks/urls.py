from django.urls import path
from apps.banks import views


urlpatterns = [
    path('load', views.LoadRatesView.as_view(), name='load_rates'),
]