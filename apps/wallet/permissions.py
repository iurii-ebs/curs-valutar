from rest_framework import permissions

from apps.wallet.models import Wallet
from apps.wallet.serializers import WalletSerializer

SAFE_METHODS = ["GET"]


class IsWalletOwner(permissions.BasePermission):
    message = "You are not the wallet owner. Permission denied"

    def has_permission(self, request, view):
        wallet_owner = Wallet.objects.get(id=view.kwargs['pk'])
        return request.user == wallet_owner.user


class IsSameCurrencyTransaction(permissions.BasePermission):
    message = "The target wallet is not of the same currency. Please use a different wallet."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        target_wallet = Wallet.objects.get(id=view.kwargs['pk'])
        return target_wallet.currency.id == request.data.get('currency')


class IsZeroBalance(permissions.BasePermission):
    message = "A wallet needs to have zero balance in order to be deleted."

    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        user_wallet = Wallet.objects.get(id=view.kwargs['pk'], user=request.user)
        return WalletSerializer(user_wallet).data['balance'] == 0.0
