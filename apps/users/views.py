from django.shortcuts import render

# Create your views here.
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from django.contrib.auth.models import User
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from apps.users import serializers
from apps.users import tokens


class RegisterView(GenericAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    @staticmethod
    def get(request):
        return Response("Input fields")

    @staticmethod
    def post(request):
        """Register new user and send email for activation"""
        serializer = serializers.UserSerializer(data=request.data)

        if serializer.is_valid():
            user_new = User.objects.create(
                first_name=serializer.validated_data['first_name'],
                last_name=serializer.validated_data['last_name'],
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email'],
                is_superuser=False,
                is_staff=False,
                is_active=False
            )
            user_new.set_password(serializer.validated_data['password'])
            user_new.save()

            # Compose email
            email_subject = render_to_string('users/account_activation_email_subject.html')
            email_message = render_to_string(
                'users/account_activation_email_body.html',
                {
                    'user': user_new,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(user_new.pk)),
                    'token': tokens.account_activation_token.make_token(user_new),
                }
            )

            # Send email
            user_new.email_user(
                subject=email_subject,
                message=email_message
            )

            return Response(
                {
                    'user_new': serializers.UserSerializer(user_new).data,
                    'message': "Please confirm your email address to complete the registration",
                }
            )

        return Response(serializer.errors)


class ActivateView(GenericAPIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request, uid_encoded, token):
        # Check if link is valid
        try:
            uid = force_text(urlsafe_base64_decode(uid_encoded))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        # Check if requested user exists and activation token is valid
        if user is None and tokens.account_activation_token.check_token(user, token):
            return Response(status.HTTP_404_NOT_FOUND)

        # Activate user
        user.is_active = True
        user.save()

        return Response({
            'user': serializers.UserSerializer(user).data,
            'message': 'User activated'
        })


class PasswordResetView(GenericAPIView):
    serializer_class = serializers.PasswordResetSerializer
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        return Response("Input email")

    @staticmethod
    def post(request):
        """Generate password reset link and send email"""
        serializer = serializers.PasswordResetSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors)

        user = User.objects.filter(email=serializer.validated_data['email']).first()

        if user is None:
            return Response("User does not exist")

        # Compose email
        email_subject = render_to_string('users/account_reset_password_email_subject.html')
        email_message = render_to_string(
            'users/account_reset_password_email_body.html',
            {
                'user': user,
                'domain': get_current_site(request).domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': tokens.password_reset_token.make_token(user),
            }
        )

        # Send email
        user.email_user(
            subject=email_subject,
            message=email_message
        )

        return Response('We send reset link to email')


class PasswordChangeView(GenericAPIView):
    serializer_class = serializers.PasswordChangeSerializer
    permission_classes = [AllowAny]

    @staticmethod
    def get(request, uid_encoded, token):
        # Check if link is valid
        try:
            uid = force_text(urlsafe_base64_decode(uid_encoded))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is None and tokens.account_activation_token.check_token(user, token):
            return Response(status.HTTP_404_NOT_FOUND)

        return Response("Input passwords")

    @staticmethod
    def post(request, uid_encoded, token):
        # Check if link is valid
        try:
            uid = force_text(urlsafe_base64_decode(uid_encoded))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is None and tokens.password_reset_token.check_token(user, token):
            return Response(status.HTTP_404_NOT_FOUND)

        # Check if request data is valid
        serializer = serializers.PasswordChangeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors)

        # Change password
        user.set_password(serializer.validated_data['password1'])
        user.save()

        return Response({
            'user': serializers.UserSerializer(user).data,
            'message': 'Password changed'
        })
