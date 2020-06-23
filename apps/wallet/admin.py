from django.contrib import admin
from apps.wallet.models import (Currency,
                                RatesHistory,
                                Wallet,
                                WalletOperations)

admin.site.register(Currency)
admin.site.register(RatesHistory)
admin.site.register(Wallet)
admin.site.register(WalletOperations)
