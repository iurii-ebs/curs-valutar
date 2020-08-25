from fcm_django.models import FCMDevice
from celery import shared_task


@shared_task(name='push_notify')
def push_notify(user, title, message):
    devices = FCMDevice.objects.filter(user=user, active=True)
    for device in devices:
        device.send_message(title, message)
