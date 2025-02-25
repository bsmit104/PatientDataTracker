from django.urls import path
from . import views

urlpatterns = [
    path('', views.patient_list, name='patient_list'),
    path('chart/', views.patient_chart, name='patient_chart'),
    path('add/', views.add_patient, name='add_patient'),
    path('edit/<int:pk>/', views.edit_patient, name='edit_patient'),
    path('delete/<int:pk>/', views.delete_patient, name='delete_patient'),
    path('patient/<int:pk>/', views.patient_detail, name='patient_detail'),
]

# from django.urls import path
# from . import views

# urlpatterns = [
#     path('', views.patient_list, name='patient_list'),
#     path('chart/', views.patient_chart, name='patient_chart'),
#     path('add/', views.add_patient, name='add_patient'),
#     path('edit/<int:pk>/', views.edit_patient, name='edit_patient'),
#     path('delete/<int:pk>/', views.delete_patient, name='delete_patient'),
# ]

