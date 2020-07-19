from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from apps.statistics.models import RatesPrediction
from config.elastic import es


@receiver(post_save, sender=RatesPrediction)
def update_es_prediction_record(sender, instance, **kwargs):
    queryset = sender.objects.get(id=instance.id)
    es.add_document(
        index='rates-prediction',
        doc_type='curs-valutar',
        document=queryset.es_doc(),
        document_id=instance.id
    )


# To do
@receiver(pre_delete, sender=RatesPrediction)
def delete_es_prediction_record(sender, instance, *args, **kwargs):
    queryset = sender.objects.get(id=instance.id)
    print('obj deleted', instance.id)
