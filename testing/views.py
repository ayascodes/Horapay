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
               serializer.save()
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

