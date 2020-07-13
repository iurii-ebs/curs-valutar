from django.shortcuts import render
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from wkhtmltopdf.views import PDFTemplateResponse

from apps.reports.tasks import gen_static_graphs_all
from apps.wallet.serializers import RatesHistorySerializer


class PDFReportView(GenericAPIView):
    authentication_classes = (JWTAuthentication,)
    permission_classes = (AllowAny,)
    template = 'reports/index.html'
    context = {}

    def get(self, request, pk):
        self.context['currency_id'] = str(pk)

        response = PDFTemplateResponse(request=request,
                                       template=self.template,
                                       filename=f"currency_id_{pk}.pdf",
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
