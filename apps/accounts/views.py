from rest_framework.views import APIView


class FirebaseTokenView(APIView):
    def post(self, request):
        return 'hi'
