from django.shortcuts import render

# Create your views here.
from django.shortcuts import redirect
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


# Main views

class RegisterView(GenericAPIView):
    serializer_class = serializers.UserSerializer
    permission_classes = (AllowAny,)
    authentication_classes = ()

    @staticmethod
    def get(request):
        return Response("Page: Register user")

    @staticmethod
    def post(request):
        """Register new user and send email for activation"""
        serializer = serializers.UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors)

        user_new = User.objects.create(**serializer.validated_data)
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

        return redirect('user_register_done')


class ActivateView(GenericAPIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request, uid_encoded, token):
        # Check if link is valid
        try:
            uid = force_text(urlsafe_base64_decode(uid_encoded))
        except(TypeError, ValueError, OverflowError):
            return Response(status.HTTP_404_NOT_FOUND)

        user = User.objects.filter(pk=uid).first()

        # Check if requested user exists and activation token is valid
        if user is None or not tokens.account_activation_token.check_token(user, token):
            return Response(status.HTTP_404_NOT_FOUND)

        # Activate user
        user.is_active = True
        user.save()

        return redirect('user_activate_done')


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

        if user is not None:
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

        return redirect('password_reset_done')


class PasswordChangeView(GenericAPIView):
    serializer_class = serializers.PasswordChangeSerializer
    permission_classes = [AllowAny]

    @staticmethod
    def get(request, uid_encoded, token):
        # Check if link is valid
        try:
            uid = force_text(urlsafe_base64_decode(uid_encoded))
        except(TypeError, ValueError, OverflowError):
            return Response(status.HTTP_404_NOT_FOUND)

        user = User.objects.filter(pk=uid).first()

        if user is None or not tokens.account_activation_token.check_token(user, token):
            return Response(status.HTTP_404_NOT_FOUND)

        return Response("Input passwords")

    @staticmethod
    def post(request, uid_encoded, token):
        # Check if link is valid
        try:
            uid = force_text(urlsafe_base64_decode(uid_encoded))
        except(TypeError, ValueError, OverflowError):
            return Response(status.HTTP_404_NOT_FOUND)

        user = User.objects.filter(pk=uid).first()

        if user is None or not tokens.account_activation_token.check_token(user, token):
            return Response(status.HTTP_404_NOT_FOUND)

        # Check if request data is valid
        serializer = serializers.PasswordChangeSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors)

        # Change password
        user.set_password(serializer.validated_data['password1'])
        user.save()

        return redirect('password_change_done')


# Redirect views

class RegisterDoneView(GenericAPIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        return Response("Page: Account is successfully registered. Please follow email link for activation.")


class ActivateDoneView(GenericAPIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        return Response("Page: Account is successfully activated.")


class PasswordResetDoneView(GenericAPIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        return Response("Page: Password reset link is send to your email.")


class PasswordChangeDoneView(GenericAPIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        return Response("Page: Password successfully changed.")
