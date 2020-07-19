from django.apps import AppConfig


class StatisticsConfig(AppConfig):
    name = 'apps.statistics'
    verbose_name = 'Statistics'

    def ready(self):
        import apps.statistics.signals
