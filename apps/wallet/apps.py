from django.apps import AppConfig
from django.conf import settings


class WalletConfig(AppConfig):
    name = 'apps.wallet'
    verbose_name = 'Wallet'

    def ready(self):
        if settings.ELASTICSEARCHENABLED:
            import apps.wallet.signals
