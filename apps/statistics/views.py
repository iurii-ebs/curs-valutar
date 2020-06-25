from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import AllowAny

from apps.statistics.predictor import predict_function

from apps.wallet.models import Currency, RatesHistory

from rest_framework import status


@api_view(['GET', 'POST'])
def predict_list(request):
    pass


@api_view(['GET', 'POST'])
def predict_detail(request, pk):
    pass


@api_view(['GET'])
@permission_classes((AllowAny,))
def prediction_days(request, pk):
    currency_items = [x.id for x in Currency.objects.all()]
    for currency_id in currency_items:
        past_rates = [x.rate for x in RatesHistory.objects.filter(currency=currency_id).order_by('date')]
        predict_function(currency_id, past_rates, pk)

    return Response(status=status.HTTP_201_CREATED)
