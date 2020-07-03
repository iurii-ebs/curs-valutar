from celery import shared_task, task
from django.template.loader import render_to_string
from django.contrib.auth.models import User


# TODO: Change to shared_task
@task.task()
def email_account_activation(user_pk, domain, uid_encoded, token):
    user = User.objects.filter(pk=user_pk).first()

    email_subject = render_to_string(
        'users/account_activation_email_subject.html',
    )

    email_message = render_to_string(
        'users/account_activation_email_body.html',
        {
            'user': user,
            'domain': domain,
            'uid': uid_encoded,
            'token': token,
        }
    )

    user.email_user(
        subject=email_subject,
        message=email_message
    )


# TODO: Change to shared_task
@task.task()
def email_password_reset(user_pk, domain, uid_encoded, token):
    user = User.objects.filter(pk=user_pk).first()

    email_subject = render_to_string(
        'users/account_reset_password_email_subject.html'
    )

    email_message = render_to_string(
        'users/account_reset_password_email_body.html',
        {
            'user': user,
            'domain': domain,
            'uid': uid_encoded,
            'token': token,
        }
    )

    user.email_user(
        subject=email_subject,
        message=email_message
    )
