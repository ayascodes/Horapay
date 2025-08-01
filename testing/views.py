import secrets
from django.contrib.auth.tokens import  default_token_generator
from django.utils.http import urlsafe_base64_decode
from rest_framework.exceptions import ValidationError, NotFound
from .emails import *
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
from datetime import datetime, timedelta
from dateutil.rrule import rrule, DAILY, MONTHLY
from django.http import HttpResponse
import locale
from django.db.models import Q
from django.contrib.auth import logout
from django.http import JsonResponse
from .utils import create_sessions_for_weeks,calculate_charge_and_sup
from rest_framework import generics, permissions
from rest_framework.parsers import MultiPartParser, FormParser
from django.core.exceptions import ValidationError as DjangoValidationError
from rest_framework.exceptions import ValidationError as DRFValidationError


# Users CRUD
class UsersList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerialize

    def get_queryset(self):
        # Filter queryset to include only users with UserType 'enseignant'
        return CustomUser.objects.filter(UserType='Enseignant')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UsersDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerialize

    def get_queryset(self):
        # Filter queryset to include only users with UserType 'enseignant'
        return CustomUser.objects.filter(UserType='Enseignant')

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # Allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    #adminlist
class AdminList(generics.ListCreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerialize

    def get_queryset(self):
        # Filter queryset to include only users with UserType admin'
        return CustomUser.objects.filter(UserType='Admin')

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class AdminDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerialize

    def get_queryset(self):
        # Filter queryset to include only users with UserType 'admin'
        return CustomUser.objects.filter(UserType='Admin')

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # Allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

# CRUD for exams
class ExamsList(generics.ListCreateAPIView):
    queryset = Exams.objects.all()
    serializer_class = ExamsSerializer
    def create(self, request, *args, **kwargs):
        # Check if request data is a list
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=[request.data], many=True)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class ExamsDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Exams.objects.all()
    serializer_class = ExamsSerializer
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # Allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

# CRUD for vacation
class VacationList(generics.ListCreateAPIView):
    queryset = Vacation.objects.all()
    serializer_class = VacationSerializer

class VacationDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Vacation.objects.all()
    serializer_class = VacationSerializer
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # Allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

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
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # Allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

# CRUD for jourferies
class JourFeriesList(generics.ListCreateAPIView):
    queryset = JourFeries.objects.all()
    serializer_class = JourFeriesSerializer


class JourFeriesDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = JourFeries.objects.all()
    serializer_class = JourFeriesSerializer
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # Allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

# CRUD for report
class ReportList(generics.ListCreateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer

class ReportDetail(generics.RetrieveUpdateAPIView):
    queryset = Report.objects.all()
    serializer_class = ReportSerializer
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # Allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class SemestreList(generics.ListCreateAPIView):
    queryset = Semestre.objects.all()
    serializer_class = SemestreSerializer
    def create(self, request, *args, **kwargs):
        # Check if request data is a list
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=[request.data], many=True)

        if serializer.is_valid():
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        def perform_create(self, serializer):
            serializer.save()

class SemestreDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Semestre.objects.all()
    serializer_class = SemestreSerializer
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # Allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        #self.perform_update(serializer)
        # Update instance and call full_clean
        for attr, value in serializer.validated_data.items():
            setattr(instance, attr, value)
        instance.full_clean()  # This calls the clean method
        instance.save()
        return Response(serializer.data)

class SemestreCurrentYearList(generics.ListAPIView):
    serializer_class = SemestreSerializer

    def get_queryset(self):
        current_year = timezone.now().year
        current_academic_year = f"{current_year-1}/{current_year}"
        return Semestre.objects.filter(annee_academique=current_academic_year)

class DepartementList(generics.ListCreateAPIView):
    queryset = Departement.objects.all()
    serializer_class = DepartementSerializer
    def create(self, request, *args, **kwargs):
        # Check if request data is a list
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=[request.data], many=True)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class DepartementDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Departement.objects.all()
    serializer_class = DepartementSerializer
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # Allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class SpecialiteList(generics.ListCreateAPIView):
    queryset = Specialite.objects.all()
    serializer_class = SpecialiteSerializer
    def create(self, request, *args, **kwargs):
        # Check if request data is a list
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=[request.data], many=True)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class SpecialiteDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Specialite.objects.all()
    serializer_class = SpecialiteSerializer
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # Allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class SalleList(generics.ListCreateAPIView):
    queryset = Salle.objects.all()
    serializer_class = SalleSerializer

    def get_queryset(self):
        queryset = Salle.objects.all()
        departement_id = self.request.query_params.get('departement')
        if departement_id:
            queryset = queryset.filter(departement_id=departement_id)
        return queryset

    def create(self, request, *args, **kwargs):
        # Check if request data is a list
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=[request.data], many=True)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class SalleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Salle.objects.all()
    serializer_class = SalleSerializer
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # Allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class PromoList(generics.ListCreateAPIView):
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer

    def get_queryset(self):
        queryset = Promo.objects.all()
        departement_id = self.request.query_params.get('departement')
        if departement_id:
            queryset = queryset.filter(departement_id=departement_id)
        return queryset
    def create(self, request, *args, **kwargs):
        # Check if request data is a list
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=[request.data], many=True)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class PromoDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Promo.objects.all()
    serializer_class = PromoSerializer
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # Allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class SectionList(generics.ListCreateAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer

    def get_queryset(self):
        queryset = Section.objects.all()
        promo_id = self.request.query_params.get('promo')
        if promo_id:
            queryset = queryset.filter(promo_id=promo_id)
        return queryset
    def create(self, request, *args, **kwargs):
        # Check if request data is a list
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=[request.data], many=True)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class SectionDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Section.objects.all()
    serializer_class = SectionSerializer
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # Allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class =GroupSerializer
    def get_queryset(self):
        queryset = Group.objects.all()
        section_id = self.request.query_params.get('section')
        if section_id:
            queryset = queryset.filter(section_id=section_id)
        return queryset
    def create(self, request, *args, **kwargs):
        # Check if request data is a list
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=[request.data], many=True)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class GroupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    serializer_class = GroupSerializer
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # Allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class ModuleList(generics.ListCreateAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    serializer_class = ModuleSerializer

    def get_queryset(self):
        queryset = Module.objects.all()
        semestre_id = self.request.query_params.get('semestre')
        promo_id = self.request.query_params.get('promo')

        if semestre_id and promo_id:
            queryset = queryset.filter(semestre_id=semestre_id, promo_id=promo_id)

        return queryset
    def create(self, request, *args, **kwargs):
        # Check if request data is a list
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=[request.data], many=True)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class ModuleDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Module.objects.all()
    serializer_class = ModuleSerializer
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # Allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)
class GradeList(generics.ListCreateAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    def create(self, request, *args, **kwargs):
        # Check if request data is a list
        if isinstance(request.data, list):
            serializer = self.get_serializer(data=request.data, many=True)
        else:
            serializer = self.get_serializer(data=[request.data], many=True)

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()

class GradeDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Grade.objects.all()
    serializer_class = GradeSerializer
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # Allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class Type_seanceList(generics.ListCreateAPIView):
    queryset = Type_seance.objects.all()
    serializer_class = Type_seanceSerializer

class Type_seanceDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Type_seance.objects.all()
    serializer_class = Type_seanceSerializer
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # Allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)


class CCPListView(generics.ListAPIView):
    queryset = CustomUser.objects.exclude(ccp__isnull=True, cle__isnull=True).values('ccp', 'cle')
    serializer_class = CCPSerializer

class EmailListView(generics.ListAPIView):
    queryset = CustomUser.objects.exclude(email__isnull=True).values('email')
    serializer_class = EmailSerializer
class RibListView(generics.ListAPIView):
    queryset = CustomUser.objects.exclude(RIB__isnull=True).values('RIB')
    serializer_class = RibSerializer
    
class UserProfilePhotoUploadView(generics.UpdateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = UserProfilePhotoSerializer
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def get_object(self):
        user = self.request.user
        if user.is_anonymous:
            # Handle anonymous user case, maybe return a dummy user or raise an error
            raise NotAuthenticated("User is not authenticated")
        return user


# this is for algorithm : 
class SessionCreateView(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data.copy()
        selectedOption = data.pop('selectedOption',None)
        if selectedOption == 'Que pour une semaine':
            serializer = ExtraSessionSerializer(data=data)
            # Your validation and saving process for WeeklySession
        elif selectedOption == 'Pour le semestre':
            serializer = WeeklySessionSerializer(data=data)
            # Your validation and saving process for ExtraSession
        else:
            return Response({"error": "Invalid value for specific_field"}, status=status.HTTPromo_400_BAD_REQUEST)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 

class WeeklySessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = weekly_session_new.objects.all()
    serializer_class = WeeklySessionSerializer
    lookup_field = 'pk'  # Assuming primary key is used as the lookup field

class ExtraSessionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = extra_session.objects.all()
    serializer_class = ExtraSessionSerializer
    lookup_field = 'pk'  # Assuming primary key is used as the lookup field

class ExtraSessionListView(generics.ListAPIView):
    queryset = extra_session.objects.all()
    serializer_class = ExtraSessionSerializer

class WeeklySessionListView(generics.ListAPIView):
    queryset = weekly_session_new.objects.all()
    serializer_class = WeeklySessionSerializer  

###############################
class GenerateSessionsView(APIView):
    def get(self, request):
        start_date = request.GET.get('start_date')
        end_date = request.GET.get('end_date')
        teacher_id = request.GET.get('teacher_id')

        if not start_date or not end_date or not teacher_id:
            return JsonResponse({'error': 'Missing parameters'}, status=400)

        create_sessions_for_weeks(start_date, end_date, int(teacher_id))
        
        generated_sessions = sessions.objects.filter(enseignant_id=teacher_id, date__range=[start_date, end_date])

        serializer = SessionsSerializer(generated_sessions, many=True)
        
        return JsonResponse({'status': 'Sessions generated successfully', 'sessions': serializer.data})
 # extra and weekly for a specific teacher id : 

class WeeklySessionForListView(generics.ListAPIView):
    serializer_class = WeeklySessionSerializer

    def get_queryset(self):
        teacher_id = self.kwargs.get('teacher_id')
        return weekly_session_new.objects.filter(enseignant_id=teacher_id)

class WeeklySessionForDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = WeeklySessionSerializer

    def get_queryset(self):
        teacher_id = self.kwargs.get('teacher_id')
        return weekly_session_new.objects.filter(enseignant_id=teacher_id)

class ExtraSessionForListView(generics.ListAPIView):
    serializer_class = ExtraSessionSerializer

    def get_queryset(self):
        teacher_id = self.kwargs.get('teacher_id')
        return extra_session.objects.filter(enseignant_id=teacher_id)
    
#algorithm de calcul :
class CalculateChargeSupView(APIView): 
    def get(self, request, teacher_id):
        date_debut = request.GET.get('date_debut')
        date_fin = request.GET.get('date_fin')

        if not date_debut or not date_fin:
            return JsonResponse({'error': 'date_debut and date_fin are required parameters.'}, status=400)

        try:
            total_charge_minutes, total_sup_minutes = calculate_charge_and_sup(date_debut, date_fin, teacher_id)
            return Response({
                'total_charge_minutes': total_charge_minutes,
                'total_sup_minutes': total_sup_minutes
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
        
def get_sessions(request):
    # Extract parameters from GET request
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    teacher_id = request.GET.get('teacher_id')

    # Validate parameters
    if not date_debut or not date_fin or not teacher_id:
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    # Convert date strings to datetime objects
    try:
        date_debut = datetime.strptime(date_debut, '%Y-%m-%d').date()
        date_fin = datetime.strptime(date_fin, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)

    # Query sessions within the date range for the given teacher
    session_list = sessions.objects.filter(date__range=[date_debut, date_fin], enseignant_id=teacher_id)
    
    # Serialize session data
    session_data = []
    for session in session_list:
        session_data.append({
            'id': session.id,
            'date': session.date,
            'selectedDay': session.selectedDay,
            'heure_debut': session.heure_debut,  # No need to convert to datetime object
            'heure_fin': session.heure_fin,      # No need to convert to datetime object
            'module': session.module.nom if session.module else None,
            'type_session': session.type_session.nom if session.type_session else None,
            'salle': session.salle.SalleName if session.salle else None,
            'is_heure_sup': session.is_heure_sup,
            'is_partially_heure_sup': session.is_partially_heure_sup,
            'duration_sup': session.duration_sup if session.is_partially_heure_sup else 0,
            'duration_charge': session.duration_charge if session.is_partially_heure_sup else 0,
        })

    # Return sessions as JSON response
    return JsonResponse({'sessions': session_data})

def get_week_with_sessions(request):
    # Extract parameters from GET request
    date_debut = request.GET.get('date_debut')
    date_fin = request.GET.get('date_fin')
    teacher_id = request.GET.get('teacher_id')

    # Validate parameters
    if not date_debut or not date_fin or not teacher_id:
        return JsonResponse({'error': 'Missing parameters'}, status=400)

    # Convert date strings to datetime objects
    try:
        date_debut = datetime.strptime(date_debut, '%Y-%m-%d').date()
        date_fin = datetime.strptime(date_fin, '%Y-%m-%d').date()
    except ValueError:
        return JsonResponse({'error': 'Invalid date format. Use YYYY-MM-DD.'}, status=400)

    # Query weeks within the date range
    weeks_with_sessions = Week.objects.filter(
        sessions__date__range=[date_debut, date_fin],
        sessions__enseignant_id=teacher_id
    ).distinct()

    # Serialize week data along with associated sessions
    week_data = []
    monthly_duration_sup = {}
    total_duration_sup = 0

    for week in weeks_with_sessions:
        session_data = []
        week_duration_sup = 0  # Calculate the total duration_sup for the week

        for session in week.sessions.filter(is_heure_sup=True) | week.sessions.filter(is_partially_heure_sup=True):
            if session.is_heure_sup:
                # Calculate session duration in hours
                session_duration = (datetime.strptime(session.heure_fin, '%H:%M') - datetime.strptime(session.heure_debut, '%H:%M')).seconds / 3600
                week_duration_sup += session_duration
            elif session.is_partially_heure_sup:
                week_duration_sup += session.duration_sup / 60  # Convert minutes to hours

            session_data.append({
                'id': session.id,
                'date': session.date.strftime('%Y-%m-%d'),  # Format date as YYYY-MM-DD
                'selectedDay': session.selectedDay,
                'heure_debut': session.heure_debut,  # No need to convert to datetime object
                'heure_fin': session.heure_fin,      # No need to convert to datetime object
                'module': session.module.nom if session.module else None,
                'type_session': session.type_session.nom if session.type_session else None,
                'salle': session.salle.SalleName if session.salle else None,
                'is_heure_sup': session.is_heure_sup,
                'is_partially_heure_sup': session.is_partially_heure_sup,
                'duration_sup': session.duration_sup if session.is_partially_heure_sup else 0,
                'duration_charge': session.duration_charge if session.is_partially_heure_sup else 0,
            })

        week_data.append({
            'week_number': week.week_number,
            'month': week.month,
            'start_date': week.start_date.strftime('%Y-%m-%d'),  # Format date as YYYY-MM-DD
            'end_date': week.end_date.strftime('%Y-%m-%d'),      # Format date as YYYY-MM-DD
            'Duration_sup': round(week_duration_sup, 2),  # Round to 2 decimal places
            'sessions': session_data,
        })

        # Accumulate monthly_duration_sup
        if week.month in monthly_duration_sup:
            monthly_duration_sup[week.month] += week_duration_sup
        else:
            monthly_duration_sup[week.month] = week_duration_sup

        # Accumulate total_duration_sup
        total_duration_sup += week_duration_sup

    # Prepare response
    response_data = {
        'weeks_with_sessions': week_data,
        'monthly_duration_sup': {month: round(duration, 2) for month, duration in monthly_duration_sup.items()},
        'total_duration_sup': round(total_duration_sup, 2)
    }

    # Return week data with associated sessions as JSON response
    return JsonResponse(response_data)



########################
class EtablissementList(generics.ListCreateAPIView):
    queryset = Etablissement.objects.all()
    serializer_class = EtablissementSerializer

class EtablissementDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Etablissement.objects.all()
    serializer_class = EtablissementSerializer
    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # Allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

class InfoHeureSupList(generics.ListCreateAPIView):
    queryset = InfoHeureSup.objects.all()
    serializer_class = InfoHeureSupSerializer

class InfoHeureSupDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = InfoHeureSup.objects.all()
    serializer_class = InfoHeureSupSerializer

    def put(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', True)  # Allow partial updates
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

#auto_completed search by full name
class CustomUserAutocompleteView(generics.ListAPIView):
    serializer_class = CustomUserSerialize
    def get_queryset(self):
        query = self.request.GET.get('q', '')
        queryset = CustomUser.objects.filter(full_name__icontains=query)
        return queryset


#filtrage grade sexe
class CustomUserFilterView(generics.ListAPIView):
    serializer_class = CustomUserSerialize

    def get_queryset(self):
        queryset = CustomUser.objects.all()

        grade_id = self.request.GET.get('grade', None)
        sexe = self.request.GET.get('sexe', None)

        filters = Q()

        if grade_id:
            filters &= Q(grade__id=grade_id)

        if sexe:
            filters &= Q(sexe=sexe)

        queryset = queryset.filter(filters)
        return queryset


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
          data = request.data.copy()
          # Handle base64 image data for 'photo_profil'
          photo_profil_data = data.get('photo_profil')
          if photo_profil_data:
              format, imgstr = photo_profil_data.split(';base64,')
              ext = format.split('/')[-1]
              data['photo_profil'] = ContentFile(base64.b64decode(imgstr), name=f'temp.{ext}')
          serializer = CustomUserSerialize(data=request.data)
          password = request.data.get('password')
          if serializer.is_valid():
              # serializer.save()
               user = serializer.save(password=password)
               user.UserType="Enseignant"
               user.full_name= f"{user.nom} {user.prenom}"
               user.is_active=True
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
   def post(self, request):
       try:
          serializer = CustomUserSerialize(data=request.data)
          password = request.data.get('password')
          if serializer.is_valid():
               #serializer.save()
               user = serializer.save(password=password)
               user.UserType = "Admin"
               user.is_admin =True
               user.is_active = True
               user.full_name = f"{user.nom} {user.prenom}"
               user.save()
               send_activation_email_admin(serializer.data['email'],password)
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


class LogoutView(APIView):
    def post(self, request):
        try:
            logout(request)
            return Response({'detail': 'Successfully logged out.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_400_BAD_REQUEST)
