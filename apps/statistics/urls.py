from django.urls import path
from django.conf import settings
from apps.statistics import views
from apps.statistics import noes_views

urlpatterns = [
    path('predict/', views.PredictListView.as_view() if settings.ELASTICSEARCHENABLED else noes_views.PredictListView.as_view(), name='predict_list'),
    path('predict/<int:pk>/', views.PredictDetailView.as_view() if settings.ELASTICSEARCHENABLED else noes_views.PredictDetailView.as_view(), name='predict_detail'),
    path('history/', views.RatesHistoryListView.as_view() if settings.ELASTICSEARCHENABLED else noes_views.RatesHistoryListView.as_view(), name='history_list'),
    path('history/<int:pk>/', views.RatesHistoryDetailView.as_view() if settings.ELASTICSEARCHENABLED else noes_views.RatesHistoryDetailView.as_view(), name='history_detail'),
    path('live/', views.RatesLiveListView.as_view() if settings.ELASTICSEARCHENABLED else noes_views.RatesLiveListView.as_view(), name='live_list'),
    path('live/<int:pk>/', views.RatesLiveDetailView.as_view() if settings.ELASTICSEARCHENABLED else noes_views.RatesLiveDetailView.as_view(), name='live_detail'),
    path('predict/<int:pk>/days/', views.PredictionDaysDetailView.as_view() if settings.ELASTICSEARCHENABLED else views.PredictionDaysDetailView.as_view(), name='prediction_days'),
]
