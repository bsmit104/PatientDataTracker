from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_list, name='patient_list'),
    path('chart/', views.patient_chart, name='patient_chart'),
]