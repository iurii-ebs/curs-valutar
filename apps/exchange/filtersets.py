from django_filters import FilterSet
from apps.exchange.models import Bank, Coin, Rate


class BankFilterSet(FilterSet):
    class Meta:
        model = Bank
        fields = {
            'id': [
                'exact', 'in',
            ],
            'registered_name': [
                'exact', 'contains',
            ],
            'short_name': [
                'exact', 'contains',
            ],
            'website': [
                'exact', 'contains',
            ],
        }


class CoinFilterSet(FilterSet):
    class Meta:
        model = Coin
        fields = {
            'id': [
                'exact', 'in',
            ],
            'name': [
                'exact', 'contains',
            ],
            'abbr': [
                'exact', 'contains',
            ],
            'bank': [
                'exact', 'in',
            ],
        }


class RateFilterSet(FilterSet):
    class Meta:
        model = Rate
        fields = {
            'id': [
                'exact', 'in',
            ],
            'rate_sell': [
                'exact', 'gt', 'lt', 'gte', 'lte',
            ],
            'rate_buy': [
                'exact', 'gt', 'lt', 'gte', 'lte',
            ],
            'date': [
                'exact', 'gt', 'lt', 'gte', 'lte',
            ],
            'currency': [
                'exact', 'in',
            ],
        }
