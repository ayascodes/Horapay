from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from . import views
from .views import *

urlpatterns = [  
    path('users/', UsersList.as_view(), name='users-list'),
    path('users/<int:pk>/', UsersDetail.as_view(), name='users-detail'),
    path('exams/', ExamsList.as_view(), name='exams-list'),
    path('exams/<int:pk>/', ExamsDetail.as_view(), name='exams-detail'),
    path('vacations/', VacationList.as_view(), name='vacation-list'),
    path('vacations/<int:pk>/', VacationDetail.as_view(), name='vacation-detail'),
    path('stages/', StageList.as_view(), name='stage-list'),
    path('stages/<int:pk>/', StageDetail.as_view(), name='stage-detail'),
    path('absences/', AbsenceList.as_view(), name='absence-list'),
    path('absences/<int:pk>/', AbsenceDetail.as_view(), name='absence-detail'),
    path('jourferies/', JourFeriesList.as_view(), name='jourferies-list'),
    path('jourferies/<int:pk>/', JourFeriesDetail.as_view(), name='jourferies-detail'),
    path('reports/', ReportList.as_view(), name='report-list'),
    path('reports/<int:pk>/', ReportDetail.as_view(), name='report-detail'),
    path('reports/<int:id>/status/', report_status, name='report-status'),
    path('semestres/', SemestreList.as_view()),
    path('semestres/<int:pk>/', SemestreDetail.as_view()),
    path('departements/', DepartementList.as_view()),
    path('departements/<int:pk>/', DepartementDetail.as_view()),
    path('Specialite/', SpecialiteList.as_view()),
    path('Specialite/<int:pk>/', SpecialiteDetail.as_view()),
    path('Salle/', SalleList.as_view()),
    path('Salle/<int:pk>/', SalleDetail.as_view()),
    path('Promo/', PromoList.as_view()),
    path('Promo/<int:pk>/', PromoDetail.as_view()),
    path('Group/', GroupList.as_view()),
    path('Group/<int:pk>/', GroupDetail.as_view()),
    path('sections/', SectionList.as_view()),
    path('sections/<int:pk>/', SectionDetail.as_view()),
    path('weekly-sessions/', WeeklySessionList.as_view()),
    path('weekly-sessions/<int:pk>/', WeeklySessionDetail.as_view()),
    path('Module/', ModuleList.as_view()),
    path('Module/<int:pk>/', ModuleDetail.as_view()),
    path('grade/', GradeList.as_view()),
    path('grade/<int:pk>/', GradeDetail.as_view()),
#registration
    path('inscription/', AjoutEnseignant.as_view(),name='inscription'),
    path('ajout_admin/',AjoutAdmin.as_view(),name='ajout_admin'),
    #login
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    #reset_password
    path('reset_password/',ResetPasswordRequestView.as_view(),name='reset_password_request'),
    path('reset-password/<str:token>/', ResetPasswordConfirmView.as_view(), name='reset_password_confirm'),










    #READ THIS (tell me if i made a mistake), see figma to know exactly what im talking about

#for frontend, i did separate urls, so i dont ruin the old ones if they dont work correctly
    
    
    
# create emploi interface:
    
    # enseignant is the same, we get them all, no need to change it
    # also semester
    # also departement


    # matiere, salle stay like they are, we get them all

    # save button in the interface is the weeklySession, need to verify if it work in both cases (semester and semaine)






# vos enseignants interface:

    # when entering the interface we get all enseignats, already done like before nothing change
    # add enseignant is the same

    # search and filters are needed
    
    #all interface below it (modifier, delete ..) are already done





# enseignant -> absences interface:
    path('enseignant_abs_count/', EnseignantAbsenceCount.as_view()),
    # ajouter absence already done





# enseignant -> paiment (here the algorithme will be used)
    #





# preferences -> departement interface:

    # no change, already done
    # in the model, we need to remove choice fields of departement (so there is no restriction, just a string)





# agenda annulle interfaces:

    #no change already done correctly






#







]
