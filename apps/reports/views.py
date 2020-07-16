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
from django.http import HttpResponse


class PDFReportView(GenericAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    template = 'reports/index.html'
    context = {}

    def get(self, request, pk):
        forecast = RatesPredictionText.objects.get(currency_id=pk)
        filename = f"currency_id_{forecast.currency.id}_{forecast.currency.abbr}_{forecast.currency.name}_{forecast.currency.bank}_{datetime.date.today()}.pdf".lower().replace(
            " ", "_")
        filepath = f"{settings.STATIC_ROOT}/pdf/"
        check_pdf_available = os.path.isfile(filepath + filename)
        if check_pdf_available:
            with open(filepath + filename, 'rb') as pdf:
                response = HttpResponse(pdf.read(), content_type='application/pdf')
                response['Content-Disposition'] = f'filename={filename}'
                return response
        else:
            save_pdf_report_files(pk, filepath, filename)

            self.context = {"currency_id": str(pk),
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


class GenPDFGraphs(GenericAPIView):
    queryset = ''
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    serializer_class = RatesHistorySerializer

    def get(self, request):
        gen_static_graphs_all()
        return Response(status=status.HTTP_202_ACCEPTED)


class PDFFileRenderView(GenericAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    template = 'reports/index.html'
    context = {}

    def get(self, request, pk):
        forecast = RatesPredictionText.objects.get(currency_id=pk)
        filename = f"currency_id_{forecast.currency.id}_{forecast.currency.abbr}_{forecast.currency.name}_{forecast.currency.bank}_{datetime.date.today()}.pdf".lower().replace(
            " ", "_")

        self.context = {"currency_id": str(pk),
                        "period": f"{datetime.date.today()} / \
                                   {datetime.date.today() + datetime.timedelta(7)}",
                        "forecast": forecast.message}

        response = PDFTemplateResponse(request=request,
                                       template=self.template,
                                       filename=filename,
                                       context=self.context,
                                       show_content_in_browser=False,
                                       cmd_options={'enable-local-file-access': True}
                                       )
        return response
