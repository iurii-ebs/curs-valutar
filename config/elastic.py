from django.conf import settings
from drf_util.elastic import ElasticUtil


class Elastic(ElasticUtil):
    hosts = settings.ELASTIC['hosts']
    index_prefix = settings.ELASTIC['index_prefix']
    activity_index = 'elastic_test'


es = Elastic()
