import secrets
from django.contrib.auth.tokens import  default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework.exceptions import ValidationError, NotFound
from .emails import send_activation_email, send_reset_password_email
from rest_framework.permissions import AllowAny,IsAdminUser,IsAuthenticated
from rest_framework.views import APIView
from rest_framework import generics, status, viewsets
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from . import validators

import logging
import time


# Users CRUD
class UsersList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerialize

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsersDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerialize

# CRUD for exams
class ExamsList(generics.ListCreateAPIView):
    queryset = Exams.objects.all()
    serializer_class = ExamsSerializer

class ExamsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exams.objects.all()
    serializer_class = ExamsSerializer

# CRUD for vacation
class VacationList(generics.ListCreateAPIView):
    queryset = Vacation.objects.all()
    serializer_class = VacationSerializer

class VacationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vacation.objects.all()
    serializer_class = VacationSerializer

# CRUD for stage
class StageList(generics.ListCreateAPIView):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer

class StageDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Stage.objects.all()
    serializer_class = StageSerializer

# CRUD for absence
class AbsenceList(generics.ListCreateAPIView):
    queryset = Absence.objects.all()
    serializer_class = AbsenceSerializer

class AbsenceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Absence.objects.all()
    serializer_class = AbsenceSerializer

# CRUD for jourferies
class JourFeriesList(generics.ListCreateAPIView):
    queryset = JourFeries.objects.all()
    serializer_class = JourFeriesSerializer

class JourFeriesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = JourFeries.objects.all()
    serializer_class = JourFeriesSerializer

# CRUD for report
class ReportList(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

class ReportDetail(generics.RetrieveUpdateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

class SemestreList(generics.ListCreateAPIView):
    queryset = Semestre.objects.all()
    serializer_class = SemestreSerializer

class SemestreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Semestre.objects.all()
    serializer_class = SemestreSerializer

class DepartementList(generics.ListCreateAPIView):
    queryset = Departement.objects.all()
    serializer_class = DepartementSerializer

class DepartementDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Departement.objects.all()
    serializer_class = DepartementSerializer

class SpecialiteList(generics.ListCreateAPIView):
    queryset = Specialite.objects.all()
    serializer_class = SpecialiteSerializer

class SpecialiteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Specialite.objects.all()
    serializer_class = SpecialiteSerializer

class SalleList(generics.ListCreateAPIView):
    queryset = Salle.objects.all()
    serializer_class = SalleSerializer

class SalleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Salle.objects.all()
    serializer_class = SalleSerializer

class PromoList(generics.ListCreateAPIView):
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer

class PromoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer

class SectionList(generics.ListCreateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

class SectionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

class ModuleList(generics.ListCreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

class ModuleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer

class GradeList(generics.ListCreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

class GradeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer

class WeeklySessionList(generics.ListCreateAPIView):
    queryset = Weekly_session.objects.all()
    serializer_class = Weekly_sessionserializer

class WeeklySessionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Weekly_session.objects.all()
    serializer_class = Weekly_sessionserializer


@api_view(['GET'])
def report_status(request, id):
    try:
        report = Report.objects.get(pk=id)
    except Report.DoesNotExist:
        return Response({"error": "Report not found"}, status=status.HTTP_404_NOT_FOUND)

#authentication
class AjoutEnseignant(APIView):
   #permission_classes = [IsAuthenticated]
   def post(self, request):
       try:
          serializer = CustomUserSerialize(data=request.data)
          password = request.data.get('password')
          if serializer.is_valid():
              # serializer.save()
               user = serializer.save(password=password)
               user.UserType="Enseignant"
               user.save()
               send_activation_email(serializer.data['email'],password)
               return Response({
               'status':200,
               'message':'votre ajout d\'enseignant est effectuer avec succes',
               'data': serializer.data,
            })
          return Response({
              'status':400,
              'message':'Une chose qu\'il n\'est pas correcte',
              'data':serializer.errors
          })
       except Exception as e:
           return Response({
               'status': 400,
               'message': 'Une chose qu\'il n\'est pas correcte',
               'data': str(e)
           })
class AjoutAdmin(APIView):
   #permission_classes = [IsAuthenticated]
   def post(self, request):
       try:
          serializer = CustomUserSerialize(data=request.data)
          password = request.data.get('password')
          if serializer.is_valid():
               #serializer.save()
               user = serializer.save(password=password)
               user.UserType = "Admin"
               user.is_admin =True
               user.save()
               send_activation_email(serializer.data['email'],password)
               return Response({
               'status':200,
               'message':'votre ajout d\'admin est effectuer avec succes',
               'data': serializer.data,
            })
          return Response({
              'status':400,
              'message':'Une chose qu\'il n\'est pas correcte',
              'data':serializer.errors
          })
       except Exception as e:
           return Response({
               'status': 400,
               'message': 'Une chose qu\'il n\'est pas correcte',
               'data': str(e)
           })




class ResetPasswordRequestView(APIView):
    permission_classes = [AllowAny]
    def post(self,request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            user = CustomUser.objects.filter(email=email).first()
            if user:
                #token= secrets.token_urlsafe(64)
                #token = token_generator.make_token(user)
                refresh = RefreshToken.for_user(user)
                token = refresh.access_token

                user.reset_password_token = token
                user.save()
                send_reset_password_email(email,token)
                return Response({'message':'un email de re-initialisation a ete envoye'})
            return Response(serializer.errors,status=400)


class ResetPasswordConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, token):
        Response.data={
            "Received token:":token
        }
        if not token:
            raise ValidationError("Token is required")

        try:
            user_id = urlsafe_base64_decode(token).decode('utf-8')
            #Response("Decoded user_id:", user_id)  # Debugging statement
            user = CustomUser.objects.get(pk=user_id)
        except (TypeError, ValueError, OverflowError):
            raise ValidationError("Invalid token format")
        except CustomUser.DoesNotExist:
            raise NotFound("User not found")

        if not default_token_generator.check_token(user, token):
            raise ValidationError("Invalid token")

        new_password = request.data.get('new_password')
        if not new_password:
            raise ValidationError("New password is required.")

        user.set_password(new_password)
        user.save()
        return Response({'message': 'Password reset successful'})



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer




class TeacherAbsenceStatsView(APIView):
    def get(self, request):
        teachers = CustomUser.objects.all()
        data = []
        for teacher in teachers:
            sessions = teacher.session_set.filter(
                #date__gte=current_semester.start_date,
                #date__lte=current_semester.end_date
            )

            justified_count = sessions.filter(occured=False).filter(absence__justified=True).count()
            unjustified_count = sessions.filter(occured=False).filter(absence__justified=False).count()
            teacher_data = {
                'id': teacher.id,
                'name': teacher.name,
                'justified_absences': justified_count,
                'unjustified_absences': unjustified_count,
            }
        data.append(teacher_data)
        return Response(data)


class EnseignantAbsenceCount(APIView):
    def get(self, request):
        """
        Retrieves all teachers with counts of justified and unjustified absences.

        Returns a JSON response with the following structure:
            {
                "teachers": [
                    {
                        "id": <teacher_id>,
                        "username": <teacher_username>,
                        "justified_absences": <count_justified_absences>,
                        "unjustified_absences": <count_unjustified_absences>,
                    },
                    ...
                ]
            }
        """

        teachers = CustomUser.objects.filter(is_admin=False)

        absence_data = []
        for teacher in teachers:
            absences = Absence.objects.filter(enseignant=teacher)
            justified_count = absences.filter(is_justified=True).count()
            unjustified_count = absences.filter(is_justified=False).count()

            absence_data.append({
                "id": teacher.id,
                "username": teacher.nom + ' ' + teacher.prenom,
                "justified_absences": justified_count,
                "unjustified_absences": unjustified_count,
            })

        return Response(absence_data)


class CalculateTeacherHours(generics.ListAPIView): # it is without a response for now
    # request need to have date_debut and date_fin
    # request need to have teacher_id
    # and then calculate what are the weeks based on date debut et fin de semestre and month


    queryset = Weekly_session.objects.all()
    serializer_class = Weekly_sessionserializer

    def calculate(self, serializer):
        semester_id = self.request.data['semester_id']
        teacher_id = self.request.data['teacher_id']
        date_debut = self.request.data['date_debut']
        date_fin = self.request.data['date_fin']


        semester = Semestre.objects.filter(id=semester_id).first()
        #semester_date_debut = semester.date_debut
        #semester_date_fin = semester.date_fin

        weeks = validators.get_weeks_between(date_debut, date_fin)

        queryset = self.queryset.filter(semestre = semester_id, enseignant= teacher_id)

        sessions_for_the_entire_semester = queryset.filter(pour = 'Pour le semestre')
        sessions_pour_la_semaine = queryset.filter(pour="Que pour une semaine")

        jour_feriers = JourFeries.objects.all()


        nbr_hours_in_each_week = []


        i = 0
        for week_debut, week_fin in weeks:
            if (i % 2 == 0):
                sessions_pour_cette_semaine = sessions_pour_la_semaine.filter(date__gte = week_debut, date_lte = week_fin)
                # here we need also the date in this week for the session_pour_cette_semain_in semester
                

                # first, we need to sort them based on session_type (for now it is just on sessions_pour_cette_semaine, after this it will be on the 2 types of pour)
                

                # now we need to compare the date if it is in a range of one of the jours feries
                # later add the other types of vacations
                for session in sessions_pour_cette_semaine:    
                    will_be_included_in_calculation = True
                    for jour_ferier in jour_feriers:
                        if (session.date >= jour_ferier.datedebut) and (session.date <= jour_ferier.datefin):
                            #mean that this session is in jour_ferier and it is not included in calculation
                            will_be_included_in_calculation = False
                            break
                    if will_be_included_in_calculation == False:
                        sessions_pour_cette_semaine.exclude(session)

                for session in sessions_for_the_entire_semester:
                    will_be_included_in_calculation = True
                    for jour_ferier in jour_feriers:
                        if (validators.get_date_for_weeklysession(week_debut, session.jour)>= jour_ferier.datedebut) and (validators.get_date_for_weeklysession(week_debut, session.jour)<= jour_ferier.datefin):
                            will_be_included_in_calculation = False
                            break
                    if will_be_included_in_calculation == False:
                        sessions_for_the_entire_semester.exclude(session)


                

                cours_Sessions_semaine = sessions_pour_cette_semaine.filter(type_session = "Cours") #these are pour semaine
                td_sessions_semaine = sessions_pour_cette_semaine.filter(type_session = "TD") #these are pour semaine
                tp_sessions_semaine = sessions_pour_cette_semaine.filter(type_session = "TP") #these are pour semaine

                cours_Sessions_this_week_semester = sessions_for_the_entire_semester.filter(type_session = "Cours") 
                td_Sessions_this_week_semester = sessions_for_the_entire_semester.filter(type_session = "TD")
                tp_Sessions_this_week_semester = sessions_for_the_entire_semester.filter(type_session = "TP")






                # maybe here the values are seperate, for cours, td, tp

                # need to parametrable later (coeffiecient of td, tp, cours), also the max_weekly_hours
                nbrHours = 0
                for cours in cours_Sessions_semaine:
                    nbr_hours = nbr_hours + (cours.heure_fin - cours.heure_debut)*2
                for cours in cours_Sessions_this_week_semester:
                    nbr_hours = nbr_hours + (cours.heure_fin - cours.heure_debut)*2


                for td in td_sessions_semaine:
                    nbr_hours = nbr_hours + (td.heure_fin - td.heure_debut)*1.5
                for td in td_Sessions_this_week_semester:
                    nbr_hours = nbr_hours + (td.heure_fin - td.heure_debut)*1.5


                for tp in tp_sessions_semaine:
                    nbr_hours = nbr_hours + (tp.heure_fin - tp.heure_debut)
                for tp in tp_Sessions_this_week_semester:
                    nbr_hours = nbr_hours + (tp.heure_fin - tp.heure_debut)


                nbr_hours_in_each_week.append(nbrHours)

                # i forget to add a list like the one above, for hours_sup and hours normal

            i = i + 1
            pass #dont know what to return for the frontend for now


