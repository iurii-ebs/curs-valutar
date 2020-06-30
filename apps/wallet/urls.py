from django.urls import path

from apps.wallet import views

urlpatterns = [
    path('', views.WalletListView.as_view(), name='wallet_list'),
    path('<int:pk>/', views.WalletDetailView.as_view(), name='wallet_detail'),
    path('<int:pk>/transactions/', views.WalletTransactionsView.as_view(), name='wallet_transactions')
]
