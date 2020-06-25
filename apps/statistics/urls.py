from django.urls import path

from apps.statistics import views

urlpatterns = [
    path('predict', views.predict_list, name='predict_list'),
    path('predict/<int:pk>/', views.predict_detail, name='predict_detail'),
]
