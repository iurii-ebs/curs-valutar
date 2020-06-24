from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.exceptions import PermissionDenied

from apps.wallet.models import (Currency,
                                RatesHistory,
                                Wallet,
                                WalletOperation)

from apps.wallet.serializers import (CurrencySerializer,
                                     RatesHistorySerializer,
                                     WalletSerializer,
                                     WalletOperationSerializer)


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticatedOrReadOnly,))
@authentication_classes((JWTAuthentication,))
def wallet_list(request):
    if request.method == 'GET':
        queryset = Wallet.objects.all()
        serializer = WalletSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        user = JWTAuthentication().authenticate(request)[0]
        serializer = WalletSerializer(data=request.data)
        if serializer.is_valid():
            wallet_new = Wallet.objects.create(
                user=user,
                currency=Currency.objects.get(abbr=serializer.validated_data['currency'])
            )
            wallet_new.save()
            return Response(WalletSerializer(wallet_new).data)
        return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes((JWTAuthentication,))
def wallet_detail(request, pk):
    pass


@api_view(['GET', 'POST'])
@permission_classes((IsAuthenticated,))
@authentication_classes((JWTAuthentication,))
def wallet_operations_list(request):
    if request.method == 'GET':
        user = JWTAuthentication().authenticate(request)[0]
        queryset = Wallet.objects.get(user=user).operationitem.all()
        serializer = WalletOperationSerializer(queryset, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        user = JWTAuthentication().authenticate(request)[0]
        serializer = WalletOperationSerializer(data=request.data)
        if serializer.is_valid():
            if user != serializer.validated_data['wallet'].user:
                raise PermissionDenied
            wallet_operation_new = WalletOperation.objects.create(
                wallet=serializer.validated_data['wallet'],
                rate=serializer.validated_data['rate'],
                amount=serializer.validated_data['amount']
            )
            wallet_operation_new.save()
            return Response(WalletOperationSerializer(wallet_operation_new).data)
        return Response(serializer.errors)


@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
@authentication_classes((JWTAuthentication,))
def wallet_operations_detail(request, pk):
    pass
