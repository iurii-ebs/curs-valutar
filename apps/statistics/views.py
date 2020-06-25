from rest_framework.decorators import api_view
from rest_framework.response import Response


@api_view(['GET', 'POST'])
def predict_list(request):
    pass


@api_view(['GET', 'POST'])
def predict_detail(request, pk):
    pass
