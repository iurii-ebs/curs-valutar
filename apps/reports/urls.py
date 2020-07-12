from django.urls import path

from apps.statistics import views

urlpatterns = [
    path('<int:pk>/', views.PDFReportView.as_view(), name='PDF_currency_report'),
]
