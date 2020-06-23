from django.urls import path

from apps.wallet import views

urlpatterns = [
    path('wallet/', views.wallet_list, name='wallet_list'),
    path('wallet/<int:pk>/', views.wallet_detail, name='wallet_detail')
]
