from django.template.loader import render_to_string
from django.contrib.auth.models import User


def email_account_activation(user_id, uid_encoded, token, domain):
    user = User.objects.filter(id=user_id).first()

    email_subject = render_to_string('users/account_activation_email_subject.html')
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


def email_password_reset():
    pass
