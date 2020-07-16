from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework_simplejwt.authentication import JWTAuthentication
from apps.statistics.models import RatesPrediction
from apps.statistics.tasks import update_rate_prediction, indexation_es_rateshistory
from apps.statistics.serializers import RatesPredictionSerializer
from apps.wallet.serializers import RatesHistorySerializer
from config.elastic import es


class RatesHistoryListView(GenericAPIView):
    queryset = ''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RatesHistorySerializer

    def get(self, request):
        body = {
            "size": 10000,
            "query": {
                "match_all": {},
            },
        }
        es_queryset = es.search(index="rates-history",
                                doc_type="curs-valutar",
                                body=body
                                )
        source = [es.get_source(history_item) for history_item in es_queryset[0]]
        return Response(source)


class PredictListView(GenericAPIView):
    queryset = ''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RatesPredictionSerializer

    def get(self, request):
        body = {
            "size": 10000,
            "query": {
                "match_all": {},
            },
        }
        es_queryset = es.search(index="rates-prediction",
                                doc_type="curs-valutar",
                                body=body
                                )
        source = [es.get_source(predict_item) for predict_item in es_queryset[0]]
        return Response(source)


class PredictDetailView(GenericAPIView):
    queryset = ''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RatesPredictionSerializer

    def get(self, request, pk):
        body = {
            "size": 10000,
            "query": {
                "term": {"currency": pk}
            },
        }
        es_queryset = es.search(index="rates-prediction",
                                doc_type="curs-valutar",
                                body=body
                                )
        source = [es.get_source(predict_item) for predict_item in es_queryset[0]]
        return Response(source)


class PredictionDaysDetailView(GenericAPIView):
    queryset = ''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RatesPredictionSerializer

    def post(self, request, pk):
        update_rate_prediction.delay(pk)
        return Response(status=status.HTTP_200_OK)
