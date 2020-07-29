from __future__ import absolute_import, unicode_literals

import os

from celery import Celery
from celery.schedules import crontab
from django.conf import settings
import datetime

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

app = Celery('config')

app.config_from_object('django.conf:settings', namespace='CELERY')

app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    print('Request: {0!r}'.format(self.request))


app.conf.timezone = settings.TIME_ZONE

app.conf.beat_schedule = {
    'create_rates_daily': {
        'task': 'create_rates',
        'schedule': crontab(minute=40, hour=9, day_of_week='1-5'),
        'args': (str(datetime.datetime.today().date()),)
    },

    'rate-prediction-daily': {
        'task': 'update_rate_prediction',
        'schedule': crontab(minute=45, hour=9, day_of_week='1-5'),
        'args': (7,)
    },

    'gen-static-graphs-all': {
        'task': 'gen_static_graphs_all',
        'schedule': crontab(minute=50, hour=9, day_of_week='1-5')
    },

    'mail_reports_daily': {
        'task': 'send_email_reports',
        'schedule': crontab(minute=0, hour=[10, 11], day_of_week='1-5')
    },
}
