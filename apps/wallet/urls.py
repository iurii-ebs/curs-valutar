from django.urls import path

from apps.wallet import views

urlpatterns = [
    path('wallet/', views.wallet_list, name='wallet_list'),
    path('wallet/<int:pk>/', views.wallet_detail, name='wallet_detail'),
    path('wallet-operation/', views.wallet_operations_list, name='wallet_operations_list'),
    path('wallet-operation/<int:pk>/', views.wallet_operations_detail, name='wallet_operations_detail')
]
