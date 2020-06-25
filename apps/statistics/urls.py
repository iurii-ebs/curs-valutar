from django.urls import path

from apps.statistics import views

urlpatterns = [
    path('predict/', views.predict_list, name='predict_list'),
    path('predict/<int:pk>/', views.predict_detail, name='predict_detail'),
    path('predict/<int:pk>/days/', views.prediction_days, name='prediction_days'),
]
