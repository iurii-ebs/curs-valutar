from django.urls import path

from apps.wallet import views

urlpatterns = [
    path('', views.wallet_list, name='wallet_list'),
    path('<int:pk>/', views.wallet_detail, name='wallet_detail'),
    path('<int:pk>/transactions/', views.wallet_transactions, name='wallet_transactions')
]
