from django.urls import path
from . import views
from .views import *

urlpatterns = [
    path("users/",views.Users_list , name="users"),
    path("users/<int:id>",views.Users_detail),

    path('exams/', views.exams_list, name='exams_list'),
    path('exams/<int:pk>/', views.exams_detail, name='exams_detail'),
    path('vacation/', views.vacation_list, name='vacation_list'),
    path('vacation/<int:pk>/', views.vacation_detail, name='vacation_detail'),
    path('stage/', views.stage_list, name='stage_list'),
    path('stage/<int:pk>/', views.stage_detail, name='stage_detail'),
    path('jourferies/',views.jour_feries_list),
    path('jourferies/<int:pk>/', views.jour_feries_detail, name='jourfries_detail'),
    path('absence/', views.absence_list, name='absence_list'),
    path('absence/<int:pk>/', views.absence_detail, name='absence_detail'),
  
    path('reports/', views.report_list),
    path('reports/<int:id>/', views.report_detail),
    path('reports/<int:id>/status/', views.report_status),
    
]
