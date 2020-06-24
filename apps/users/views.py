from django.shortcuts import render

# Create your views here.
from django.contrib.auth.models import User
from drf_util.decorators import serialize_decorator
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes

from apps.users.serializers import UserSerializer


class RegisterUserView(GenericAPIView):
    serializer_class = UserSerializer

    permission_classes = (AllowAny,)
    authentication_classes = ()

    @serialize_decorator(UserSerializer)
    def post(self, request):
        validated_data = request.serializer.validated_data

        user = User.objects.create(
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            username=validated_data['username'],
            is_superuser=True,
            is_staff=True
        )
        user.set_password(validated_data['password'])
        user.save()

        return Response(UserSerializer(user).data)


@api_view(http_method_names=['POST', 'GET'])
@permission_classes([AllowAny])
def register_user_view(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            validated_data = serializer.validated_data

            user_new = User.objects.create(
                first_name=validated_data['first_name'],
                last_name=validated_data['last_name'],
                username=validated_data['username'],
                is_superuser=True,
                is_staff=True
            )
            user_new.set_password(validated_data['password'])
            user_new.save()

            return Response(UserSerializer(user_new).data)

        return Response(serializer.errors)