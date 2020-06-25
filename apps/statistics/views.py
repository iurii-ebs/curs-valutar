from datetime import datetime, timedelta


from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from apps.wallet.models import RatesHistory
from apps.wallet.serializers import RatesHistorySerializer


@api_view(['GET', 'POST'])
def predict_list(request):
    pass


@api_view(['GET', 'POST'])
def predict_detail(request, pk):
    pass


@api_view(['GET'])
@permission_classes([AllowAny])
def progress_detail_view(request, pk, days=7):
    date_to = datetime.today()
    date_from = date_to - timedelta(days=7)

    queryset = RatesHistory.objects.filter(
        currency=pk,
        date__range=[date_from, date_to]
    )
    serializer = RatesHistorySerializer(queryset, many=True)

    return Response(serializer.data)
