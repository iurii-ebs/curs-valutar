from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from wkhtmltopdf.views import PDFTemplateResponse
import datetime
from django.conf import settings
import os
from apps.reports.tasks import gen_static_graphs_all, save_pdf_report_files
from apps.wallet.serializers import RatesHistorySerializer
from apps.statistics.models import RatesPredictionText


class PDFReportView(GenericAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    template = 'reports/index.html'
    context = {}

    def get(self, request, pk):
        forecast = RatesPredictionText.objects.get(currency_id=pk)
        filename = f"currency_id_{forecast.currency.id}_{forecast.currency.abbr}_{forecast.currency.name}_{forecast.currency.bank}.pdf".lower().replace(" ", "_")
        filepath = f"{settings.STATIC_ROOT}/pdf/"
        save_pdf_report_files(filepath, filename)

        self.context['context'] = {"currency_id": str(pk),
                                   "period": f"{datetime.date.today()} / \
                                   {datetime.date.today() + datetime.timedelta(7)}",
                                   "forecast": forecast.message}

        response = PDFTemplateResponse(request=request,
                                       template=self.template,
                                       filename=filename,
                                       context=self.context,
                                       show_content_in_browser=True,
                                       cmd_options={'enable-local-file-access': True}
                                       )
        return response


# Test view for quick graph generation - to be deleted
class GenPDFGraphs(GenericAPIView):
    queryset = ''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RatesHistorySerializer

    def get(self, request):
        gen_static_graphs_all()
        return Response(status=status.HTTP_202_ACCEPTED)
