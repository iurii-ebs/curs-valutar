from django.conf import settings
from elasticsearch import Elasticsearch

es = Elasticsearch(hosts=settings.ELASTIC['hosts'], timeout=50)


def get_source(es_queryset):
    source = [hit['_source'] for hit in es_queryset['hits']['hits']]
    return source
