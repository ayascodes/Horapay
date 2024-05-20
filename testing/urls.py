from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .views import *


urlpatterns = [  
    path('users/', UsersList.as_view(), name='users-list'),
    path('users/<int:pk>', UsersDetail.as_view(), name='users-detail'),
    path('exams/', ExamsList.as_view(), name='exams-list'),
    path('exams/<int:pk>', ExamsDetail.as_view(), name='exams-detail'),
    path('vacations/', VacationList.as_view(), name='vacation-list'),
    path('vacations/<int:pk>', VacationDetail.as_view(), name='vacation-detail'),
    path('stages/', StageList.as_view(), name='stage-list'),
    path('stages/<int:pk>', StageDetail.as_view(), name='stage-detail'),
    path('absences/', AbsenceList.as_view(), name='absence-list'),
    path('absences/<int:pk>', AbsenceDetail.as_view(), name='absence-detail'),
    path('jourferies/', JourFeriesList.as_view(), name='jourferies-list'),
    path('jourferies/<int:pk>', JourFeriesDetail.as_view(), name='jourferies-detail'),
    path('reports/', ReportList.as_view(), name='report-list'),
    path('reports/<int:pk>', ReportDetail.as_view(), name='report-detail'),
    path('reports/<int:id>/status/', report_status, name='report-status'),
    path('semestres/', SemestreList.as_view()),
    path('semestres/<int:pk>', SemestreDetail.as_view()),
    path('departements/', DepartementList.as_view()),
    path('departements/<int:pk>', DepartementDetail.as_view()),
    path('Specialite/', SpecialiteList.as_view()),
    path('Specialite/<int:pk>', SpecialiteDetail.as_view()),
    path('Salle/', SalleList.as_view()),
    path('Salle/<int:pk>', SalleDetail.as_view()),
    path('Promo/', PromoList.as_view()),
    path('Promo/<int:pk>', PromoDetail.as_view()),
    path('Group/', GroupList.as_view()),
    path('Group/<int:pk>', GroupDetail.as_view()),
    path('sections/', SectionList.as_view()),
    path('sections/<int:pk>', SectionDetail.as_view()),
    path('weekly-sessions/', WeeklySessionList.as_view()),
    path('weekly-sessions/<int:pk>', WeeklySessionDetail.as_view()),
    ##
    #path('sections/<int:pk>', SectionDetail.as_view()),
    path('sessions/', SessionCreateView.as_view(), name='session-create'),
    path('sessions/weekly/<int:pk>/', WeeklySessionDetailView.as_view(), name='weekly-session-detail'),
    path('sessions/extra/<int:pk>/', ExtraSessionDetailView.as_view(), name='extra-session-detail'),
    path('sessions/extra/', ExtraSessionListView.as_view(), name='extra-session-list'),
    path('sessions/weekly/', WeeklySessionListView.as_view(), name='weekly-session-list'),
    path('generate-sessions/', GenerateSessionsView.as_view(), name='generate-sessions'),
    path('sessions/extra_for/<int:teacher_id>/', ExtraSessionForListView.as_view(), name='extra-session-list'),
    path('sessions/weekly_for/<int:teacher_id>/', WeeklySessionForListView.as_view(), name='weekly-session-list'),
    path('sessions/weekly_for/<int:teacher_id>/<int:pk>/', WeeklySessionForDetailView.as_view(), name='weekly-session-detail'),
    path('calcul_for/<int:teacher_id>/', CalculateChargeSupView.as_view(), name='calculate_charge_sup'),
    path('Module/', ModuleList.as_view()),
    path('Module/<int:pk>', ModuleDetail.as_view()),
    path('grade/', GradeList.as_view()),
    path('grade/<int:pk>', GradeDetail.as_view()),
    path('Etablissement/', EtablissementList.as_view()),
    path('Etablissement/<int:pk>', EtablissementDetail.as_view()),
    path('MaxHeureSup/', MaxHeureSupList.as_view()),
    path('MaxHeureSup/<int:pk>', MaxHeureSupDetail.as_view()),
    path('users/autocomplete/', CustomUserAutocompleteView.as_view(), name='user-autocomplete'),
    path('users/filtrage/',CustomUserFilterView.as_view(),name='user-filtrage'),
    path('admin/',AdminList.as_view()),
    path('admin/<int:pk>', AdminDetail.as_view()),
    path('type_seance/', Type_seanceList.as_view()),
    path('type_seance/<int:pk>', Type_seanceDetail.as_view()),

#registration
    path('inscription/', AjoutEnseignant.as_view(),name='inscription'),
    path('ajout_admin',AjoutAdmin.as_view(),name='ajout_admin'),
    #login
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #logout
    path('logout/',LogoutView.as_view(),name='logout'),

    #reset_password
    path('reset_password/',ResetPasswordRequestView.as_view(),name='reset_password_request'),
    path('reset-password/<str:token>/', ResetPasswordConfirmView.as_view(), name='reset_password_confirm'),
    #date en jours
    path('date-range/', DateRangeView.as_view(), name='date_range'),
# urls.py




]
