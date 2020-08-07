from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.statistics.models import RatesPrediction
from apps.statistics.tasks import update_rate_prediction
from apps.statistics.serializers import RatesPredictionSerializer
from apps.wallet.serializers import RatesHistorySerializer
from apps.wallet.models import RatesHistory


class RatesLiveListView(GenericAPIView):
    queryset = ''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RatesHistorySerializer

    def get(self, request):
        queryset = RatesHistory.objects.order_by("currency_id", 'date').reverse().distinct("currency_id")
        serializer = RatesHistorySerializer(queryset, many=True)
        return Response(serializer.data)


class RatesLiveDetailView(GenericAPIView):
    queryset = ''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RatesHistorySerializer

    def get(self, request, pk):
        queryset = RatesHistory.objects.filter(currency_id=pk).latest('date')
        serializer = RatesHistorySerializer(queryset)
        return Response(serializer.data)


class RatesHistoryListView(GenericAPIView):
    queryset = ''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RatesHistorySerializer

    def get(self, request):

        queryset = RatesHistory.objects.all().order_by('date').reverse()
        serializer = RatesHistorySerializer(queryset, many=True)
        return Response(serializer.data)


class RatesHistoryDetailView(GenericAPIView):
    queryset = ''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RatesHistorySerializer

    def get(self, request, pk):

        queryset = RatesHistory.objects.filter(currency=pk).order_by('date').reverse()
        serializer = RatesHistorySerializer(queryset, many=True)
        return Response(serializer.data)


class PredictListView(GenericAPIView):
    queryset = ''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RatesPredictionSerializer

    def get(self, request):
        queryset = RatesPrediction.objects.all().order_by('date').reverse()
        serializer = RatesPredictionSerializer(queryset, many=True)
        return Response(serializer.data)


class PredictDetailView(GenericAPIView):
    queryset = ''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RatesPredictionSerializer

    def get(self, request, pk):
        queryset = RatesPrediction.objects.filter(currency=pk).order_by('date').reverse()
        serializer = RatesPredictionSerializer(queryset, many=True)
        return Response(serializer.data)


class PredictionDaysDetailView(GenericAPIView):
    queryset = ''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RatesPredictionSerializer

    def post(self, request, pk):
        update_rate_prediction.delay(pk)
        return Response(status=status.HTTP_200_OK)
