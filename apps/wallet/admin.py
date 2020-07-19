from django.contrib import admin

from apps.wallet.models import (
    Bank,
    Currency,
    RatesHistory,
    Wallet,
    WalletOperation)

admin.site.register(Bank)
admin.site.register(Currency)
admin.site.register(RatesHistory)
admin.site.register(Wallet)
admin.site.register(WalletOperation)
