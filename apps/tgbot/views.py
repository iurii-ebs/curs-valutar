from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from .dispacher import process_new_updates


class WebHookView(APIView):
    permission_classes = [AllowAny]

    @staticmethod
    def post(request):
        process_new_updates(request)
        return Response()
