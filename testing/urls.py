from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .views import *

urlpatterns = [  
    path('users/', views.UsersList.as_view(), name='users-list'),
    path('users/<int:pk>/', views.UsersDetail.as_view(), name='users-detail'),
    path('exams/', views.ExamsList.as_view(), name='exams-list'),
    path('exams/<int:pk>/', views.ExamsDetail.as_view(), name='exams-detail'),
    path('vacations/', views.VacationList.as_view(), name='vacation-list'),
    path('vacations/<int:pk>/', views.VacationDetail.as_view(), name='vacation-detail'),
    path('stages/', views.StageList.as_view(), name='stage-list'),
    path('stages/<int:pk>/', views.StageDetail.as_view(), name='stage-detail'),
    path('absences/', views.AbsenceList.as_view(), name='absence-list'),
    path('absences/<int:pk>/', views.AbsenceDetail.as_view(), name='absence-detail'),
    path('jourferies/', views.JourFeriesList.as_view(), name='jourferies-list'),
    path('jourferies/<int:pk>/', views.JourFeriesDetail.as_view(), name='jourferies-detail'),
    path('reports/', views.ReportList.as_view(), name='report-list'),
    path('reports/<int:pk>/', views.ReportDetail.as_view(), name='report-detail'),
    path('reports/<int:id>/status/', views.report_status, name='report-status'),
    path('semestres/', views.SemestreList.as_view()),
    path('semestres/<int:pk>/', views.SemestreDetail.as_view()),
    path('departements/', views.DepartementList.as_view()),
    path('departements/<int:pk>/', views.DepartementDetail.as_view()),
    path('Specialite/', views.SpecialiteList.as_view()),
    path('Specialite/<int:pk>/', views.SpecialiteDetail.as_view()),
    path('Salle/', views.SalleList.as_view()),
    path('Salle/<int:pk>/', views.SalleDetail.as_view()),
    path('Promo/', views.PromoList.as_view()),
    path('Promo/<int:pk>/', views.PromoDetail.as_view()),
    path('sections/', views.SectionList.as_view()),
    path('sections/<int:pk>/', views.SectionDetail.as_view()),
    path('weekly-sessions/', views.WeeklySessionList.as_view()),
    path('weekly-sessions/<int:pk>/', views.WeeklySessionDetail.as_view()),
#registration
    path('inscription/', AjoutEnseignant.as_view(),name='inscription'),
    #login
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #reset_password
    path('reset_password/',ResetPasswordRequestView.as_view(),name='reset_password_request'),
    path('reset-password/<str:token>/', ResetPasswordConfirmView.as_view(), name='reset_password_confirm'),


]
