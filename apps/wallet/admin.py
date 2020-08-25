from django.contrib import admin

from apps.wallet.models import (
    Bank,
    Currency,
    RatesHistory,
    Wallet,
    WalletOperation)


@admin.register(Bank)
class BankAdmin(admin.ModelAdmin):
    list_display = ('id', 'registered_name', 'short_name', 'website', 'logo_path',)
    search_fields = ('id', 'registered_name', 'short_name', 'website', 'logo_path',)


@admin.register(Currency)
class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('id', 'bank', 'name', 'abbr',)
    search_fields = ('id', 'bank', 'name', 'abbr',)


@admin.register(RatesHistory)
class RatesHistoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'currency', 'rate_sell', 'rate_buy', 'date',)
    search_fields = ('id',)


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'currency',)
    search_fields = ('id', 'user__username', 'currency',)


@admin.register(WalletOperation)
class WalletOperationAdmin(admin.ModelAdmin):
    list_display = ('id', 'wallet', 'currency', 'rate', 'amount',)
    search_fields = ('id', 'wallet', 'rate', 'amount',)
