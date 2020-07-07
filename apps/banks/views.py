from datetime import datetime, timedelta

from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework.response import Response

from .models import Bank, Coin, Rate, Load
from .serializers import BankSerializer, CoinSerializer, RateSerializer, LoadSerializer
from .permissions import IsStaffOrReadOnly
from .tasks import create_rates


class LoadViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Load.objects.all()
    serializer_class = LoadSerializer
    permission_classes = [IsAdminUser]

    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors)
        create_rates.delay(date=str(serializer.validated_data['date']))

        return Response({
            'ok': True,
            'detail': 'Load rates request is sent',
        })


class BankViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Bank.objects.all()
    serializer_class = BankSerializer
    permission_classes = [IsStaffOrReadOnly]

    @action(detail=True)
    def list_coins(self, request, pk):
        coins = Coin.objects.filter(bank=self.get_object())
        return Response(CoinSerializer(coins, many=True).data)


class CoinViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Coin.objects.all()
    serializer_class = CoinSerializer
    permission_classes = [IsStaffOrReadOnly]

    @action(detail=True)
    def list_rates(self, request, pk):
        rates = Rate.objects.filter(currency=self.get_object())
        return Response(RateSerializer(rates, many=True).data)

    @action(detail=True)
    def list_rates_from(self, request, pk, days=7):
        date_to = datetime.today()
        date_from = date_to - timedelta(days=days)
        rates = Rate.objects.filter(
            currency=self.get_object(),
            date__range=[date_from, date_to]
        )
        return Response(RateSerializer(rates, many=True).data)


class RateViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    permission_classes = [IsStaffOrReadOnly]
