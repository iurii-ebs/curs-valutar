from __future__ import absolute_import, unicode_literals
import os
from django.conf import settings
from celery import Celery
from celery.schedules import crontab

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.timezone = settings.TIME_ZONE

app.conf.beat_schedule = {
    'rate-prediction-daily': {
        'task': 'update_rate_prediction',
        'schedule': crontab(minute="48", hour="17"),
        'args': (7,)
    },
    'elasticsearch-indexation-rates_history': {
        'task': 'indexation_es_rateshistory',
        'schedule': crontab(minute="55", hour="8")
    },
    'elasticsearch-indexation_es_ratesprediction': {
        'task': 'indexation_es_ratesprediction',
        'schedule': crontab(minute="55", hour="8")
    },
    'gen-static-graphs-all': {
        'task': 'gen_static_graphs_all',
        'schedule': crontab(minute="55", hour="8")
    },
    'create_rates_daily': {
        'task': 'create_rates',
        'schedule': crontab(minute="40", hour="8")
    }
    # ,
    # 'mail_reports_daily': {
    #     'task': 'send_email_reports',
    #     'schedule': crontab(minute="05", hour="9")
    # }
}
