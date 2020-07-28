from django.apps import AppConfig
from django.conf import settings


class StatisticsConfig(AppConfig):
    name = 'apps.statistics'
    verbose_name = 'Statistics'

    def ready(self):
        if settings.ELASTICSEARCHENABLED:
            import apps.statistics.signals
