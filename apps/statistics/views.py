from datetime import datetime, timedelta


from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView

from apps.wallet.models import RatesHistory
from apps.wallet.serializers import RatesHistorySerializer


@api_view(['GET', 'POST'])
def predict_list(request):
    pass


@api_view(['GET', 'POST'])
def predict_detail(request, pk):
    pass


class ProgressDetailView(GenericAPIView):
    serializer_class = RatesHistorySerializer
    permission_classes = [AllowAny]

    @staticmethod
    def get(request, pk, days):
        date_to = datetime.today()
        date_from = date_to - timedelta(days=days)

        queryset = RatesHistory.objects.filter(
            currency=pk,
            date__range=[date_from, date_to]
        )
        serializer = RatesHistorySerializer(queryset, many=True)

        return Response(serializer.data)
