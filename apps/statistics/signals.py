from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from apps.statistics.models import RatesPrediction
from config.elastic import es
import elasticsearch

@receiver(post_save, sender=RatesPrediction)
def update_es_prediction_record(sender, instance, **kwargs):
    queryset = sender.objects.get(id=instance.id)
    es.index(
        index='curs-valutar-ratesprediction',
        body=queryset.es_doc(),
        id=instance.id
    )


@receiver(pre_delete, sender=RatesPrediction)
def delete_es_prediction_record(sender, instance, *args, **kwargs):
    try:
        es.delete(
            index='curs-valutar-ratesprediction',
            id=instance.id
        )
    except elasticsearch.NotFoundError as es_not_found:
        print('NotFoundError, please check logs:', instance.id, es_not_found)
        pass
