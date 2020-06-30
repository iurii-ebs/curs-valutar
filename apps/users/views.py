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
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        """
        @api {get} /users/register/ Request registration page
        @apiName RegisterView
        @apiGroup Users
        """
        return Response("Page: Registration page")

    @staticmethod
    def post(request):
        """
        @api {post} /users/register/ Request user registration
        @apiName RegisterView
        @apiGroup Users
        @apiParam {String} first_name User's first_name.
        @apiParam {String} last_name User's last_name.
        @apiParam {String} email User's email.
        @apiParam {String} username User's username.
        @apiParam {String} password User's password.
        @apiSuccess redirect to /users/register-done/
        """
        serializer = serializers.UserSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors)

        # Create new user
        user_new = User.objects.create(is_active=False, **serializer.validated_data)
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
        """
        @api {get} /users/activate/encoded_uid/token Request user activation
        @apiName ActivateView
        @apiGroup Users
        """
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
        """
        @api {get} /users/password-reset/ Request password reset
        @apiName PasswordResetView
        @apiGroup Users
        """
        return Response("Page: Reset password page")

    @staticmethod
    def post(request):
        """
        @api {post} /users/password-reset/ Confirm password reset
        @apiName PasswordResetView
        @apiGroup Users
        @apiParam {String} email User's email.
        """
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
        """
        @api {get} /users/password-change/uid_encoded/token Request password change page
        @apiName PasswordChangeView
        @apiGroup Users
        """
        # Check if link is valid
        try:
            uid = force_text(urlsafe_base64_decode(uid_encoded))
        except(TypeError, ValueError, OverflowError):
            return Response(status.HTTP_404_NOT_FOUND)

        user = User.objects.filter(pk=uid).first()

        if user is None or not tokens.account_activation_token.check_token(user, token):
            return Response(status.HTTP_404_NOT_FOUND)

        return Response("Page: password change page")

    @staticmethod
    def post(request, uid_encoded, token):
        """
        @api {post} /users/password-change/uid_encoded/token Request password change page
        @apiName PasswordChangeView
        @apiGroup Users
        @apiParam {String} password1 User's new password.
        @apiParam {String} password2 User's new password confirm.
        """
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
        """
        @api {get} /users/register-done/ Request register-done page
        @apiName RegisterDoneView
        @apiGroup Users
        """
        return Response("Page: Account is successfully registered. Please follow email link for activation.")


class ActivateDoneView(GenericAPIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        """
        @api {get} /users/activate-done/ Request activate-done page
        @apiName ActivateDoneView
        @apiGroup Users
        """
        return Response("Page: Account is successfully activated.")


class PasswordResetDoneView(GenericAPIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        """
        @api {get} /users/password-reset-done/ Request password-reset-done page
        @apiName PasswordResetDoneView
        @apiGroup Users
        """
        return Response("Page: Password reset link is send to your email.")


class PasswordChangeDoneView(GenericAPIView):
    permission_classes = [AllowAny]

    @staticmethod
    def get(request):
        """
        @api {get} /users/password-change-done/ Request password-change-done page
        @apiName PasswordChangeDoneView
        @apiGroup Users
        """
        return Response("Page: Password successfully changed.")
