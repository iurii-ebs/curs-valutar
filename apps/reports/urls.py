from django.urls import path

from apps.reports import views

urlpatterns = [
    path('<int:pk>', views.PDFReportView.as_view(), name='pdf_currency_report'),
    path('gen/<int:pk>', views.GenPDFGraphs.as_view(), name='gen_pdf_graphs'),
    path('test/<int:pk>', views.NormalView.as_view(), name='test_currency_report'),
]
