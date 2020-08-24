from django.contrib.auth import get_user_model

from rest_framework.mixins import CreateModelMixin
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny

from rest_framework_simplejwt.tokens import RefreshToken

from firebase_admin import credentials, auth, initialize_app
from firebase_admin.auth import (
    InvalidIdTokenError,
    ExpiredIdTokenError,
    RevokedIdTokenError,
    CertificateFetchError,
)

from apps.accounts import serializers


User = get_user_model()

EMAIL_VERIFICATION = False

firebase_admin_config = credentials.Certificate('firebase-admin-config.json')
admin_app = initialize_app(firebase_admin_config)


class FirebaseTokenView(CreateModelMixin, GenericAPIView):
    """ Check token in firebase """
    permission_classes = [AllowAny]
    serializer_class = serializers.FirebaseTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors)

        # Validate firebase-token
        try:
            payload = auth.verify_id_token(
                id_token=serializer.validated_data['token'],
                check_revoked=True,
            )
        except ValueError:
            raise AuthenticationFailed('Token is not a string or is empty')

        except ExpiredIdTokenError:
            raise AuthenticationFailed('Specified token has expired')

        except RevokedIdTokenError:
            raise AuthenticationFailed('Token has been revoked')

        except InvalidIdTokenError:
            raise AuthenticationFailed('Token is not a valid Firebase ID token')

        except CertificateFetchError:
            raise AuthenticationFailed('An error occurs while fetching the public key certificates')

        # Check if sign_in_provider is not anonymous
        if payload["firebase"]["sign_in_provider"] == "anonymous":
            raise AuthenticationFailed('Firebase anonymous sign-in is not supported')

        # Check that email is confirmed
        if EMAIL_VERIFICATION:
            if not payload["email_verified"]:
                raise AuthenticationFailed('User email not yet confirmed')

        # Try to get user by uid
        user = User.objects.filter(
            **{User.USERNAME_FIELD: payload['uid']}
        ).first()

        # If doesn't exist, create one
        if user is None:
            firebase_user = auth.get_user(payload['uid'])
            user = User.objects.create(**{
                User.USERNAME_FIELD: payload['uid'],
                'email': firebase_user.email,
            })

        # Crete access/refresh token pair for user and return it
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
