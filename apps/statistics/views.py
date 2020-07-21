from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.statistics.serializers import RatesPredictionSerializer
from apps.statistics.tasks import update_rate_prediction
from apps.wallet.serializers import RatesHistorySerializer
from config.elastic import es, get_queryset_source


class RatesLiveListView(GenericAPIView):
    queryset = ''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RatesHistorySerializer

    def get(self, request):
        body = {
            "sort": [
                {"date": "desc"},
                "_score"
            ],
            "size": 10,
            "query": {
                "match_all": {}
            },
            "collapse": {
                "field": "currency",
                "inner_hits": {
                    "_source": {
                        "includes": []
                    },
                    "name": "currency",
                    "size": 1
                }
            }
        }
        es_queryset = es.search(index="curs-valutar-rateshistory",
                                body=body
                                )
        es_queryset = get_queryset_source(es_queryset)
        return Response(es_queryset)


class RatesLiveDetailView(GenericAPIView):
    queryset = ''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RatesPredictionSerializer

    def get(self, request, pk):
        body = {
            "sort": [
                {"date": "desc"},
                "_score"
            ],
            "size": 1,
            "query": {
                "match": {
                    "currency": pk
                }
            },
        }
        es_queryset = es.search(index="curs-valutar-rateshistory",
                                body=body,
                                )
        es_queryset = get_queryset_source(es_queryset)
        return Response(es_queryset)


class RatesHistoryListView(GenericAPIView):
    queryset = ''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RatesHistorySerializer

    def get(self, request):
        body = {
            "sort": [
                {"date": "desc"},
                "_score"
            ],
            "size": 10000,
            "query": {
                "match_all": {},
            },
        }
        es_queryset = es.search(index="curs-valutar-rateshistory",
                                body=body
                                )
        es_queryset = get_queryset_source(es_queryset)
        return Response(es_queryset)


class RatesHistoryDetailView(GenericAPIView):
    queryset = ''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RatesHistorySerializer

    def get(self, request, pk):
        body = {
            "sort": [
                {"date": "desc"},
                "_score"
            ],
            "size": 10000,
            "query": {
                "term": {"currency": pk}
            },
        }
        es_queryset = es.search(index="curs-valutar-rateshistory",
                                body=body
                                )
        es_queryset = get_queryset_source(es_queryset)
        return Response(es_queryset)


class PredictListView(GenericAPIView):
    queryset = ''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RatesPredictionSerializer

    def get(self, request):
        body = {
            "sort": [
                {"date": "desc"},
                "_score"
            ],
            "size": 10000,
            "query": {
                "match_all": {},
            },
        }
        es_queryset = es.search(index="curs-valutar-ratesprediction",
                                body=body
                                )
        es_queryset = get_queryset_source(es_queryset)
        return Response(es_queryset)


class PredictDetailView(GenericAPIView):
    queryset = ''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RatesPredictionSerializer

    def get(self, request, pk):
        body = {
            "sort": [
                {"date": "desc"},
                "_score"
            ],
            "size": 10000,
            "query": {
                "term": {"currency": pk}
            },
        }
        es_queryset = es.search(index="curs-valutar-ratesprediction",
                                body=body
                                )
        es_queryset = get_queryset_source(es_queryset)
        return Response(es_queryset)


class PredictionDaysDetailView(GenericAPIView):
    queryset = ''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RatesPredictionSerializer

    def post(self, request, pk):
        update_rate_prediction.delay(pk)
        return Response(status=status.HTTP_200_OK)
