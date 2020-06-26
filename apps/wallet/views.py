from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from django.shortcuts import get_list_or_404
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from datetime import date as datecreated

from apps.wallet.models import (Currency,
                                RatesHistory,
                                Wallet,
                                WalletOperation)

from apps.wallet.serializers import (CurrencySerializer,
                                     RatesHistorySerializer,
                                     WalletSerializer,
                                     WalletSerializerCreate,
                                     WalletOperationSerializer,
                                     WalletOperationSerializerCreate)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
@authentication_classes((JWTAuthentication,))
def wallet_list(request):
    if request.method == 'GET':
        queryset = Wallet.objects.filter(user=request.user)
        serializer = WalletSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = WalletSerializerCreate(data=request.data)
        if serializer.is_valid():
            wallet_new = Wallet.objects.create(
                user=request.user,
                currency=serializer.validated_data['currency']
            )
            wallet_new.save()
            return Response(WalletSerializerCreate(wallet_new).data)
        return Response(serializer.errors)


@api_view(['GET', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes((JWTAuthentication,))
def wallet_detail(request, pk):
    if request.method == 'GET':
        queryset = get_list_or_404(Wallet, Q(id=pk) & Q(user=request.user))
        serializer = WalletSerializer(queryset, many=True)
        return Response(serializer.data)
    elif request.method == 'DELETE':
        user_wallet = Wallet.objects.get(Q(id=pk) & Q(user=request.user))
        if WalletSerializer(user_wallet).data['balance'] == 0.0:
            user_wallet.delete()
        else:
            raise PermissionDenied
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
def wallet_transactions(request, pk):
    if request.method == 'GET':
        queryset = Wallet.objects.get(Q(user=request.user) & Q(id=pk)).operationitem.all()
        serializer = WalletOperationSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        user_wallet = Wallet.objects.get(id=pk)
        serializer = WalletOperationSerializerCreate(data=request.data)
        if serializer.is_valid():
            if request.user != user_wallet.user:
                raise PermissionDenied
            if user_wallet.currency.id != serializer.validated_data['rate'].id:
                raise PermissionDenied
            rate_today = RatesHistory.objects.get(Q(currency=serializer.validated_data['rate'].id) & Q(date=datecreated.today()))
            wallets_transactions_new = WalletOperation.objects.create(
                wallet=user_wallet,
                rate=rate_today,
                amount=serializer.validated_data['amount']
            )
            wallets_transactions_new.save()
            return Response(WalletOperationSerializerCreate(wallets_transactions_new).data)
        return Response(serializer.errors)
