from django.urls import path

from apps.statistics import views

urlpatterns = [
    path('predict', views.PredictListView.as_view(), name='predict_list'),
    path('predict/<int:pk>/', views.PredictDetailView.as_view(), name='predict_detail'),
    path('progress/<int:pk>/<int:days>/', views.ProgressDetailView.as_view(), name='progress_detail'),
    path('predict/<int:pk>/days/', views.PredictionDaysDetailView.as_view(), name='prediction_days'),
]
