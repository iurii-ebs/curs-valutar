from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from apps.statistics.models import RatesPrediction
from config.elastic import es


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
    es.delete(
        index='curs-valutar-ratesprediction',
        id=instance.id
    )
