from django.urls import path
from . import views

urlpatterns = [
    path('parse/', views.parse_currency, name='parse_url'),                                 # Save to db actual info
    path('parse/currency_first/', views.parse_currency_first, name='currency_first_url'),   # Write to DB list of names and abbrs


]
