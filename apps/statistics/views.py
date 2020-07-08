from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.statistics.models import RatesPrediction
from apps.statistics.predictor import task_update_rate_prediction
from apps.statistics.serializers import RatesPredictionSerializer


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
        task_update_rate_prediction.delay(pk)
        return Response(status=status.HTTP_200_OK)
