from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework_simplejwt.authentication import JWTAuthentication

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
def wallet_detail(request, pk):
    pass
