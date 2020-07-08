from django.urls import path

from .views import BankViewSet, CoinViewSet, RateViewSet, LoadViewSet

urlpatterns = [
    path('load/', LoadViewSet.as_view(actions={'get': 'list', 'post': 'create'}), name='load_list'),
    path('bank/', BankViewSet.as_view(actions={'get': 'list'}), name='bank-list'),
    path('coin/', CoinViewSet.as_view(actions={'get': 'list'}), name='coin-list'),
    path('rate/', RateViewSet.as_view(actions={'get': 'list'}), name='rate-list'),

    path('coin/<int:bank_id>/',
         CoinViewSet.as_view(actions={'get': 'list_coins_of_bank'}),
         name='coins_of_bank'),

    path('rate/<int:coin_id>/',
         RateViewSet.as_view(actions={'get': 'list_rates_of_coin'}),
         name='rates_of_coin'),

    path('rate/<int:coin_id>/<int:days>/',
         RateViewSet.as_view(actions={'get': 'list_rates_of_coin_from'}),
         name='rates_of_coin_from')
]
