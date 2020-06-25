from django.shortcuts import render

# Create your views here.
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from apps.users.serializers import UserSerializer
from apps.users.tokens import account_activation_token


class RegisterUserView(GenericAPIView):
    serializer_class = UserSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    @staticmethod
    def post(request):
        serializer = UserSerializer(data=request.data)

        user = User.objects.create(
            first_name=serializer.validated_data['first_name'],
            last_name=serializer.validated_data['last_name'],
            username=serializer.validated_data['username'],
            is_superuser=True,
            is_staff=True
        )
        user.set_password(serializer.validated_data['password'])
        user.save()

        return Response(UserSerializer(user).data)


"""
{
    "first_name": "Artiom",
    "last_name": "Rotari",
    "email": "ordersone@gmail.com",
    "username": "codegod",
    "password": "qwe123"
}
"""


@api_view(http_method_names=['POST'])
@permission_classes([AllowAny])
def register_user_view(request):
    serializer = UserSerializer(data=request.data)

    if serializer.is_valid():
        validated_data = serializer.validated_data

        # Register new user
        user_new = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            email=validated_data['email'],
            username=validated_data['username'],
            is_superuser=False,
            is_staff=False,
            is_active=False
        )
        user_new.set_password(validated_data['password'])
        user_new.save()

        # Compose user activation email
        activation_address = user_new.email
        activation_subject = render_to_string('users/account_activation_email_subject.html')
        activation_message = render_to_string(
            'users/account_activation_email_body.html',
            {
                'user': user_new,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user_new.pk)),
                'token': account_activation_token.make_token(user_new),
            }
        )

        # Send user activation email
        email = EmailMessage(
            subject=activation_subject,
            body=activation_message,
            to=[activation_address]
        )
        email.send()

        return Response(
            {
                'user_new': UserSerializer(user_new).data,
                'message': "Please confirm your email address to complete the registration",
            }
        )

    return Response(serializer.errors)


@api_view(http_method_names=['GET'])
@permission_classes([AllowAny])
def activate_user_view(request, uid_encoded, token):
    try:
        uid = force_text(urlsafe_base64_decode(uid_encoded))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        return Response('Thank you for your email confirmation. Now you can login your account.')
    else:
        return Response('Activation link is invalid!')
