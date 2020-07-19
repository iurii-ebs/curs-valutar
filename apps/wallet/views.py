from rest_framework import status
from rest_framework.response import Response
from django.shortcuts import get_list_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
import datetime
from rest_framework import generics, permissions
from apps.wallet.permissions import IsWalletOwner, IsSameCurrencyTransaction, IsZeroBalance

from apps.wallet.models import (RatesHistory,
                                Wallet,
                                WalletOperation)

from apps.wallet.serializers import (WalletSerializer,
                                     WalletSerializerCreate,
                                     WalletOperationSerializer,
                                     WalletOperationSerializerCreate)


class WalletListView(generics.GenericAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    serializer_class = WalletSerializer

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
            return Response(WalletSerializerCreate(wallet_new).data)
        return Response(serializer.errors)


class WalletDetailView(generics.GenericAPIView):
    queryset = ''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsZeroBalance)
    serializer_class = WalletSerializer

    def get(self, request, pk):
        queryset = get_list_or_404(Wallet, id=pk, user=request.user)
        serializer = WalletSerializer(queryset, many=True)
        return Response(serializer.data)

    def delete(self, request, pk):
        queryset = Wallet.objects.get(id=pk, user=request.user)
        queryset.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class WalletTransactionsView(generics.GenericAPIView):
    queryset = ''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsWalletOwner, IsSameCurrencyTransaction)
    serializer_class = WalletOperationSerializer

    def get(self, request, pk):
        queryset = Wallet.objects.get(user=request.user, id=pk).operationitem.all()
        serializer = WalletOperationSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        queryset = Wallet.objects.get(id=pk)
        serializer = WalletOperationSerializerCreate(data=request.data)
        if serializer.is_valid():
            rate_today = RatesHistory.objects.filter(currency=serializer.validated_data['currency'].id,
                                                     date=datetime.date.today()).latest('id')
            wallets_transactions_new = WalletOperation.objects.create(
                wallet=queryset,
                currency=serializer.validated_data['currency'],
                rate=rate_today,
                amount=serializer.validated_data['amount']
            )
            return Response(WalletOperationSerializerCreate(wallets_transactions_new).data)
        return Response(serializer.errors)
