from django.urls import path

from apps.reports import views

urlpatterns = [
    path('<int:pk>', views.PDFReportView.as_view(), name='pdf_currency_report'),
    path('gen', views.GenPDFGraphs.as_view(), name='gen_pdf_graphs'),
]
