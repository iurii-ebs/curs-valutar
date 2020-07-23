from datetime import datetime, timedelta

from rest_framework.decorators import action
from rest_framework.generics import QuerySet
from rest_framework.mixins import ListModelMixin
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet, ReadOnlyModelViewSet

from .models import Bank, Coin, Rate, Load
from .permissions import IsStaffOrReadOnly
from .serializers import BankSerializer, CoinSerializer, RateSerializer, LoadSerializer
from .tasks import create_rates


def paginate(func):
    """ Decorator used to make custom actions able for pagination """

    def decorator(self, *args, **kwargs):
        queryset = func(self, *args, **kwargs)

        if not isinstance(queryset, (list, QuerySet)):
            raise ValueError("apply_pagination expects a List or a QuerySet")

        page = self.paginate_queryset(queryset)

        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    return decorator


class DefaultPagination(PageNumberPagination):
    """ Default pagination class """
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 50


class LoadViewSet(ListModelMixin, GenericViewSet):
    """ Test endpoint used to force request data from parser """
    queryset = Load.objects.all()
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = LoadSerializer

    def create(self, request):
        serializer = self.get_serializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors)

        create_rates.delay(date=str(serializer.validated_data['date']))

        return Response({
            'ok': True,
            'detail': 'Load rates request is sent',
        })


class BankViewSet(ReadOnlyModelViewSet):
    queryset = Bank.objects.all()
    permission_classes = [IsStaffOrReadOnly]
    serializer_class = BankSerializer
    pagination_class = DefaultPagination


class CoinViewSet(ReadOnlyModelViewSet):
    queryset = Coin.objects.all()
    permission_classes = [IsStaffOrReadOnly]
    serializer_class = CoinSerializer
    pagination_class = DefaultPagination

    @paginate
    @action(methods=['GET'], detail=False)
    def list_coins_of_bank(self, request, bank_id):
        queryset = self.get_queryset().filter(bank__id=bank_id)
        return queryset


class RateViewSet(ListModelMixin, GenericViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer
    permission_classes = [IsStaffOrReadOnly]
    pagination_class = DefaultPagination

    @paginate
    @action(methods=['GET'], detail=False)
    def list_rates_of_coin(self, request, coin_id):
        queryset = self.get_queryset().filter(currency__id=coin_id)
        return queryset

    @paginate
    @action(methods=['GET'], detail=False)
    def list_rates_of_coin_from(self, request, coin_id, days=7):
        date_to = datetime.today().date()
        date_from = date_to - timedelta(days=days)
        queryset = self.get_queryset().filter(currency__id=coin_id, date__range=[date_from, date_to])
        return queryset
