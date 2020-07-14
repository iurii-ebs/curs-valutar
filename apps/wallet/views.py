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
        """
        @api {get} /wallets/:id/transactions/ Get Wallets TransactionHistory
        @apiName GetTransactionHistory
        @apiGroup Wallets
        @apiDescription Get transaction history from the user wallet

        @apiHeader {String} Content-Type=application/json
        @apiHeader {String} Authorization="Bearer <JWT token>"
        @apiParam {Number} amount Transaction amount (can be negative).
        @apiParam {Number} currency Currency id to transfer.

        @apiSuccess {JSON} object containing status as success and object message
        @apiError {JSON} object containing status as failed and error message

        @apiSuccessExample Success Response (Example):
        {
            "id": 11,
            "wallet": {
                "id": 1,
                "user": 1,
                "currency": 1,
                "balance": 228309,
                "value_buy": 4085856.9,
                "value_sell": 4018238.4,
                "profit": -67618.5
            },
            "amount": 1111,
            "currency": 1,
            "rate": 7
        }

        @apiErrorExample Error Response (Example):
        {
        "detail": "The target wallet is not of the same currency. Please use a different wallet."
        }

        @apiSampleRequest http://127.0.0.1:8000/wallets/1/transactions/
        """
        queryset = Wallet.objects.get(user=request.user, id=pk).operationitem.all()
        serializer = WalletOperationSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request, pk):
        """
        @api {post} /wallets/:id/transactions/ Post Wallets Transactions
        @apiName PostTransactions
        @apiGroup Wallets
        @apiDescription Post transactions in the user wallet

        @apiHeader {String} Content-Type=application/json
        @apiHeader {String} Authorization="Bearer <JWT token>"
        @apiParam {Number} amount Transaction amount (can be negative).
        @apiParam {Number} currency Currency id to transfer.

        @apiSuccess {JSON} object containing status as success and object message
        @apiError {JSON} object containing status as failed and error message

        @apiSuccessExample Success Response (Example):
        {
            "id": 11,
            "wallet": {
                "id": 1,
                "user": 1,
                "currency": 1,
                "balance": 228309,
                "value_buy": 4085856.9,
                "value_sell": 4018238.4,
                "profit": -67618.5
            },
            "amount": 1111,
            "currency": 1,
            "rate": 7
        }

        @apiErrorExample Error Response (Example):
        {
        "detail": "The target wallet is not of the same currency. Please use a different wallet."
        }

        @apiSampleRequest http://127.0.0.1:8000/wallets/1/transactions/
        """
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
