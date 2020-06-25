from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.statistics.predictor import predict_function

from apps.wallet.models import Currency, RatesHistory
from apps.statistics.models import RatesPrediction
from apps.statistics.serializers import RatesPredictionSerializer

from rest_framework import status


@api_view(['GET'])
@permission_classes((AllowAny,))
def predict_list(request):
    queryset = RatesPrediction.objects.all()
    serializer = RatesPredictionSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['GET'])
@permission_classes((AllowAny,))
def predict_detail(request, pk):
    queryset = RatesPrediction.objects.filter(currency=pk)
    serializer = RatesPredictionSerializer(queryset, many=True)
    return Response(serializer.data)


@api_view(['POST'])
@permission_classes((AllowAny,))
def prediction_days(request, pk):
    RatesPrediction.objects.all().delete()
    currency_items = [x.id for x in Currency.objects.all()]
    for currency_id in currency_items:
        past_rates = [x.rate for x in RatesHistory.objects.filter(currency=currency_id).order_by('date')]
        predict_function(currency_id, past_rates, pk)

    return Response(status=status.HTTP_201_CREATED)
