from django.urls import path
from .views import BankViewSet, CoinViewSet, RateViewSet, LoadViewSet


actions_load = {
    'get': 'list',
    'post': 'create',
}

actions_list = {
    'get': 'list',
}

actions_detail = {
    'get': 'retrieve',
}


urlpatterns = [
    path('load/', LoadViewSet.as_view(actions=actions_load), name='load_list'),
    path('bank/', BankViewSet.as_view(actions=actions_list), name='bank-list'),
    path('coin/', CoinViewSet.as_view(actions=actions_list), name='coin-list'),
    path('rate/', RateViewSet.as_view(actions=actions_list), name='rate-list'),
    path('bank/<int:pk>/', BankViewSet.as_view(actions=actions_detail), name='bank-detail'),
    path('coin/<int:pk>/', CoinViewSet.as_view(actions=actions_detail), name='coin-detail'),
    path('rate/<int:pk>/', RateViewSet.as_view(actions=actions_detail), name='rate-detail'),
    path('bank/<int:pk>/coins/', BankViewSet.as_view(actions={'get': 'list_coins'}), name='bank-list-coins'),
    path('coin/<int:pk>/rates/', CoinViewSet.as_view(actions={'get': 'list_rates'}), name='coin-list-rates'),
    path('coin/<int:pk>/rates/<int:days>', CoinViewSet.as_view(actions={'get': 'list_rates_from'}), name='coin-list-rates-from'),
]
