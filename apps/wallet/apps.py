from django.apps import AppConfig


class WalletConfig(AppConfig):
    name = 'apps.wallet'
    verbose_name = 'Wallet'

    def ready(self):
        import apps.wallet.signals
