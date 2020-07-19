from django.db.models.signals import post_save, pre_delete
from django.dispatch import receiver

from apps.wallet.models import RatesHistory
from config.elastic import es


@receiver(post_save, sender=RatesHistory)
def update_es_history_record(sender, instance, **kwargs):
    queryset = sender.objects.get(id=instance.id)
    es.add_document(
        index='rates-history',
        doc_type='curs-valutar',
        document=queryset.es_doc(),
        document_id=instance.id
    )


# To do
@receiver(pre_delete, sender=RatesHistory)
def delete_es_history_record(sender, instance, *args, **kwargs):
    queryset = sender.objects.get(id=instance.id)
    print('obj deleted', instance.id)
