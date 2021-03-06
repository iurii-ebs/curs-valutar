import datetime

import pdfkit
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.authentication import JWTAuthentication

from apps.reports.tasks import gen_static_graphs_all
from apps.statistics.models import RatesPredictionText
from apps.wallet.serializers import RatesHistorySerializer


class GenPDFGraphs(GenericAPIView):
    queryset = ''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RatesHistorySerializer

    def get(self, request):
        gen_static_graphs_all()
        return Response(status=status.HTTP_200_OK)


class PDFReportViewNew(GenericAPIView):
    queryset = ''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    template = 'reports/index.html'
    context = {}
    serializer_class = RatesHistorySerializer

    def get(self, request, pk):
        forecast = RatesPredictionText.objects.filter(currency_id=pk).latest('date_created')
        filename = f"currency_id_{forecast.currency.id}_{forecast.currency.abbr}_{forecast.currency.name}_\
{forecast.currency.bank}_{datetime.date.today()}.pdf".lower().replace(" ", "_")
        filepath = f"{settings.STATIC_ROOT}/pdf/"
        fake_static = f"{settings.STATIC_ROOT}graphs/"

        self.context = {"currency_id": fake_static + str(pk),
                        "period": f"{datetime.date.today()} / \
                                   {datetime.date.today() + datetime.timedelta(7)}",
                        "forecast": forecast.message,
                        "fake_static": fake_static}
        template = get_template('reports/index.html')
        html = template.render(self.context)
        options = {
            'page-size': 'Letter',
            'encoding': "UTF-8",
            'enable-local-file-access': ""
        }

        pdfkit.from_string(html, filepath + filename, options)
        pdf = pdfkit.from_string(html, False, options)
        response = HttpResponse(pdf, content_type='application/pdf')
        response['Content-Disposition'] = f'filename={filename}'
        return response
