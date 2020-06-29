from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from django.shortcuts import get_list_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.exceptions import PermissionDenied
from datetime import date as datecreated
from rest_framework.generics import GenericAPIView

from apps.wallet.models import (RatesHistory,
                                Wallet,
                                WalletOperation)

from apps.wallet.serializers import (WalletSerializer,
                                     WalletSerializerCreate,
                                     WalletOperationSerializer,
                                     WalletOperationSerializerCreate)


class WalletListView(GenericAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request):
        queryset = Wallet.objects.filter(user=request.user)
        serializer = WalletSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = WalletSerializerCreate(data=request.data)
        if serializer.is_valid():
            wallet_new = Wallet.objects.create(
                user=request.user,
                currency=serializer.validated_data['currency']
            )
            wallet_new.save()
            return Response(WalletSerializerCreate(wallet_new).data)
        return Response(serializer.errors)


class WalletDetailView(GenericAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, pk):
        queryset = get_list_or_404(Wallet, id=pk, user=request.user)
        serializer = WalletSerializer(queryset, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        user_wallet = Wallet.objects.get(id=pk, user=request.user)
        if WalletSerializer(user_wallet).data['balance'] == 0.0:
            user_wallet.delete()
        else:
            raise PermissionDenied
        return Response(status=status.HTTP_204_NO_CONTENT)


class WalletTransactionsView(GenericAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get(self, request, pk):
        queryset = Wallet.objects.get(user=request.user, id=pk).operationitem.all()
        serializer = WalletOperationSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        user_wallet = Wallet.objects.get(id=pk)
        serializer = WalletOperationSerializerCreate(data=request.data)
        if serializer.is_valid():
            if request.user != user_wallet.user:
                raise PermissionDenied
            if user_wallet.currency.id != serializer.validated_data['rate'].id:
                raise PermissionDenied
            rate_today = RatesHistory.objects.get(currency=serializer.validated_data['rate'].id,
                                                  date=datecreated.today())
            wallets_transactions_new = WalletOperation.objects.create(
                wallet=user_wallet,
                rate=rate_today,
                amount=serializer.validated_data['amount']
            )
            wallets_transactions_new.save()
            return Response(WalletOperationSerializerCreate(wallets_transactions_new).data)
        return Response(serializer.errors)
