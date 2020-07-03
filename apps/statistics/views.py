from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.statistics.models import RatesPrediction
from apps.statistics.predictor import predict_function
from apps.statistics.serializers import RatesPredictionSerializer

from apps.wallet.models import Currency, RatesHistory


class PredictListView(GenericAPIView):
    queryset = ''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RatesPredictionSerializer

    def get(self, request):
        queryset = RatesPrediction.objects.all()
        serializer = RatesPredictionSerializer(queryset, many=True)
        return Response(serializer.data)


class PredictDetailView(GenericAPIView):
    queryset = ''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RatesPredictionSerializer

    def get(self, request, pk):
        queryset = RatesPrediction.objects.filter(currency=pk)
        serializer = RatesPredictionSerializer(queryset, many=True)
        return Response(serializer.data)


class PredictionDaysDetailView(GenericAPIView):
    queryset = ''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RatesPredictionSerializer

    def post(self, request, pk):
        RatesPrediction.objects.all().delete()
        currency_items = [currency_item.id for currency_item in Currency.objects.all()]
        for currency_id in currency_items:
            past_rates = [past_rate.rate_sell for past_rate in RatesHistory.objects.filter(currency=currency_id).order_by('date')]
            predict_function.delay(currency_id, past_rates, pk)

        return Response(status=status.HTTP_201_CREATED)
